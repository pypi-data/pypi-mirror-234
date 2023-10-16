#!/usr/bin/env python3

################################################
#
#   pipeline_deploy, from YAML format
#
#   Michele Berselli - berselli.michele@gmail.com
#
################################################

import os, sys, subprocess
import shutil
import json
import glob
import boto3
import structlog
from dcicutils import ff_utils, s3_utils
from dcicutils.codebuild_utils import CodeBuildUtils
from pipeline_utils.lib import yaml_parser


###############################################################
#   REPOSITORY
#
### Expected structure for the pipeline repository
#
#   pipeline
#       descriptions
#       dockerfiles
#            <image>
#                Dockerfile
#       portal_objects
#           workflows
#               <workflow>.yaml
#           metaworkflows
#               <metaworkflow>.yaml
#           file_format.yaml
#           file_reference.yaml
#           software.yaml
#       PIPELINE
#       VERSION
#
###############################################################


###############################################################
#   Logger
###############################################################
logger = structlog.getLogger(__name__)


###############################################################
#   PostPatchRepo, class definition
###############################################################
class PostPatchRepo(object):
    """Class to handle deployment of pipeline components.
    """

    def __init__(self, args, repo, version='VERSION', pipeline='PIPELINE'):
        """Constructor method.

            :param args: Command line arguments
            :type args: object returned by ArgumentParser.parse_args() method
            :param repo: Name of the repository
            :type repo: str
            :param version: Name of the file storing pipeline version information
            :type version: str
            :param pipeline: Name of the file storing pipeline name information
            :type pipeline: str
        """
        # Init attributes
        self.ff_key = None
        self.kms_key_id = None
        self.repo = repo
        self.object_ = {
            'Software': yaml_parser.YAMLSoftware,
            'FileFormat': yaml_parser.YAMLFileFormat,
            'FileReference': yaml_parser.YAMLFileReference,
            'Workflow': yaml_parser.YAMLWorkflow,
            'MetaWorkflow': yaml_parser.YAMLMetaWorkflow
        }
        self.filepath = {
            # .yaml files
            'Software': 'portal_objects/software.yaml',
            'FileFormat': 'portal_objects/file_format.yaml',
            'FileReference': 'portal_objects/file_reference.yaml',
            # .yml files
            'Software_yml': 'portal_objects/software.yml',
            'FileFormat_yml': 'portal_objects/file_format.yml',
            'FileReference_yml': 'portal_objects/file_reference.yml',
            # folders
            'Workflow': 'portal_objects/workflows',
            'MetaWorkflow': 'portal_objects/metaworkflows',
            'ECR': 'dockerfiles',
            'WFL': 'descriptions'
        }

        # Load attributes
        for key, val in vars(args).items():
            setattr(self, key, val)

        # Get pipeline version
        with open(f'{self.repo}/{version}') as f:
            self.version = f.readlines()[0].strip()
        # Get pipeline name
        with open(f'{self.repo}/{pipeline}') as f:
            self.pipeline = f.readlines()[0].strip()

        # Load credentials
        self._get_credentials()
        self._codebuild = CodeBuildUtils()

    def _get_credentials(self):
        """Get auth credentials.
        """
        # Get portal credentials
        if os.path.exists(self.keydicts_json):
            with open(os.path.expanduser(self.keydicts_json)) as keyfile:
                keys = json.load(keyfile)
            self.ff_key = keys.get(self.ff_env)
        elif os.environ.get('GLOBAL_ENV_BUCKET') and os.environ.get('S3_ENCRYPT_KEY'):
            s3 = s3_utils.s3Utils(env=self.ff_env)
            self.ff_key = s3.get_access_keys('access_key_admin')
        else:
            raise Exception('Required deployment vars GLOBAL_ENV_BUCKET and/or S3_ENCRYPT_KEY not set, and no entry for specified enivornment exists in keydicts file.')

        # Get encryption key
        self.kms_key_id = os.environ.get('S3_ENCRYPT_KEY_ID', None)

    def _post_patch_json(self, data_json, type):
        """Helper to POST|PATCH JSON object.
        """
        # Use uuid if available as unique identifier,
        #   else use the alias
        uuid = data_json.get('uuid', data_json['aliases'][0])

        if not self.debug:
            is_patch = True
            try:
                ff_utils.get_metadata(uuid, key=self.ff_key)
            except Exception:
                is_patch = False

            # Exception for uploading of FileReference objects
            #   status -> uploading, uploaded
            #   default is None -> the status will not be updated during patch,
            #     and set to uploading if post for the first time
            if type == 'FileReference':
                # main status
                if data_json['status'] is None:
                    if is_patch:
                        del data_json['status']
                    else: # is first time post
                        data_json['status'] = 'uploading'

                # extra_files status
                extra_files_ = []
                for ext in data_json['extra_files']:
                    ext_ = {
                        'file_format': ext,
                        'status': data_json.get('status', 'uploaded')
                    }
                    extra_files_.append(ext_)
                data_json['extra_files'] = extra_files_
            ###########################################################

            if is_patch:
                ff_utils.patch_metadata(data_json, uuid, key=self.ff_key)
            else:
                ff_utils.post_metadata(data_json, type, key=self.ff_key)

            logger.info('> Posted %s' % data_json['aliases'][0])

        if self.verbose:
            logger.info(json.dumps(data_json, sort_keys=True, indent=2))

    def _yaml_to_json(self, data_yaml, YAMLClass, **kwargs):
        """Helper to validate YAML object and convert to JSON.
        """
        if self.validate:
            logger.info('> Validating %s' % data_yaml.get('name'))
            try:
                YAMLClass(data_yaml).to_json(**kwargs)
            except yaml_parser.ValidationError as e:
                # log errors
                for error in e.errors:
                    logger.error('- ValidationError [{0}]: {1} in path={2}, schema={3}'.format(
                                    error.validator,
                                    error.message,
                                    error.relative_path,
                                    error.schema
                                    )
                                )
        else:
            logger.info('> Processing %s' % data_yaml.get('name'))
            return YAMLClass(data_yaml).to_json(**kwargs)

        return

    def _post_patch_file(self, type):
        """
            'Software', 'FileFormat', 'FileReference'
        """
        logger.info(f'@ {type}...')

        # Set general variables
        filepath_ = f'{self.repo}/{self.filepath[type]}'

        # Check .yaml
        if not os.path.isfile(filepath_):

            # Check .yml
            type_yml = f'{type}_yml'
            filepath_ = f'{self.repo}/{self.filepath[type_yml]}'
            if not os.path.isfile(filepath_):
                logger.error(f'WARNING: {self.filepath[type]} or .yml not found in {self.repo}, skipping...')
                return

        # Read YAML file and create JSON objects from documents in file
        for d in yaml_parser.load_yaml(filepath_):
            # creating JSON object
            d_ = self._yaml_to_json(
                        d, self.object_[type],
                        institution=self.institution,
                        project=self.project
                        )
            # post/patch object
            if d_: self._post_patch_json(d_, type)


    def _post_patch_folder(self, type):
        """
            'Workflow', 'MetaWorkflow'
        """
        logger.info(f'@ {type}...')

        # Set general variables
        filepath_ = f'{self.repo}/{self.filepath[type]}'

        # Check
        if not os.path.isdir(filepath_):
            logger.error(f'WARNING: {self.filepath[type]} not found in {self.repo}, skipping...')
            return

        # Create JSON objects
        files_ = glob.glob(f'{filepath_}/*.yaml')
        files_.extend(glob.glob(f'{filepath_}/*.yml'))
        for fn in files_:
            for d in yaml_parser.load_yaml(fn):
                # creating _yaml_to_json **kwargs
                kwargs_ = {
                    'version': self.version,
                    'institution': self.institution,
                    'project': self.project
                }
                if type == 'Workflow':
                    kwargs_.setdefault(
                        'wflbucket_url', f's3://{self.wfl_bucket}/{self.pipeline}/{self.version}'
                    )
                # creating JSON object
                d_ = self._yaml_to_json(
                            d, self.object_[type],
                            **kwargs_
                            )
                # post/patch object
                if d_:
                    self._post_patch_json(d_, type)

    def _post_patch_wfl(self, type='WFL'):
        """
        """
        logger.info('@ Workflow Description...')

        # Set general variables
        filepath_ = f'{self.repo}/{self.filepath[type]}'
        upload_ = f'{filepath_}/upload'
        account_ = f'{self.account}.dkr.ecr.{self.region}.amazonaws.com'
        update_ = {
            'ServerSideEncryption': 'aws:kms',
            'SSEKMSKeyId': self.kms_key_id
            }

        # Check
        if not os.path.isdir(filepath_):
            logger.error(f'WARNING: {self.filepath[type]} not found in {self.repo}, skipping...')
            return

        # Create s3 object
        s3 = boto3.resource('s3')

        # Make tmp dir for upload
        if os.path.isdir(upload_):
            shutil.rmtree(upload_)
        os.mkdir(upload_)

        # Read description files and create modified files for upload
        #   placeholder variables will be replaced
        #   with specific values for the target environment
        files_ = glob.glob(f'{filepath_}/*.cwl')
        files_.extend(glob.glob(f'{filepath_}/*.wdl'))
        for fn in map(os.path.basename, files_):
            logger.info('> Processing %s' % fn)
            # set file specific variables
            file_ = f'{filepath_}/{fn}'
            upload_file_ = f'{upload_}/{fn}'
            s3_file_ = f'{self.pipeline}/{self.version}/{fn}'
            if not self.debug:
                # create modified description file for upload
                with open(file_, 'r') as read_:
                    with open(upload_file_, 'w') as write_:
                        # replace generic variables
                        for line in read_:
                            line = line.replace('ACCOUNT', account_)
                            line = line.replace('VERSION', self.version)
                            if self.sentieon_server:
                                line = line.replace('LICENSEID', self.sentieon_server)
                            write_.write(line)
                # upload to s3
                extra_args = {'ACL': 'public-read'}  # note that this is no longer public if using encryption!
                if self.kms_key_id:
                    extra_args.update(update_)
                s3.meta.client.upload_file(upload_file_, self.wfl_bucket, s3_file_, ExtraArgs=extra_args)
                logger.info('> Posted %s' % s3_file_)
                # delete file to allow tmp folder to be deleted at the end
                os.remove(upload_file_)

        # Clean tmp directory
        os.rmdir(upload_)

    def _post_patch_ecr(self, type='ECR'):
        """
        """
        logger.info('@ Docker Image...')

        # Set general variables
        filepath_ = f'{self.repo}/{self.filepath[type]}'
        account_ = f'{self.account}.dkr.ecr.{self.region}.amazonaws.com'

        # Check
        if not os.path.isdir(filepath_):
            logger.error(f'WARNING: {self.filepath[type]} not found in {self.repo}, skipping...')
            return

        # Create ecr object
        ecr = boto3.client('ecr')
        response = ecr.describe_repositories()

        # Generic bash commands to be modified to correct version and account information
        for fn in map(os.path.basename, glob.glob(f'{filepath_}/*')):
            logger.info('> Processing %s' % fn)
            if not self.debug:
                # set specific variables
                tag_ = f'{account_}/{fn}:{self.version}'
                path_ = f'{filepath_}/{fn}'
                is_repository = False
                # check if tag is present in ECR repositories,
                #   if not create it
                for repository in response['repositories']:
                    if repository['repositoryArn'].split('/')[-1] == fn:
                        is_repository = True
                        break
                if not is_repository:
                    logger.info('> Creating ECR Repository %s' % fn)
                    ecr.create_repository(repositoryName=fn)
                # build and push the image
                #   do so by local build or triggering a CodeBuild run
                build_projects = self._codebuild.list_projects()
                if self.builder:
                    builder_ = self.builder
                else:
                    builder_ = f'{self.ff_env}-pipeline-builder'
                builder = list(filter(lambda b: builder_ == b, build_projects))
                if self.local_build:
                    # TODO
                    #   enable amd/arm build
                    image = f"""
                            aws ecr get-login-password --region {self.region} | docker login --username AWS --password-stdin {account_}
                            docker build -t {tag_} {path_} --no-cache
                            docker push {tag_}
                        """ # note that we are ALWAYS doing no-cache builds so that we can get updated base images whenever applicable
                    subprocess.check_call(image, shell=True)
                elif not builder:
                    logger.error('NOTE: no builder job found in Build projects!')
                else:
                    self._codebuild.run_project_build_with_overrides(
                        project_name=builder[0], # there should only be one
                        branch=self.branch, # this is the branch to use
                        env_overrides={
                            'IMAGE_REPO_NAME': fn,
                            'IMAGE_TAG': self.version,
                            'BUILD_PATH': path_
                        }
                    )

    def run_post_patch(self):
        """Main function to deploy specified components.
        """
        # Software
        if self.post_software:
            self._post_patch_file('Software')

        # FileFormat
        if self.post_file_format:
            self._post_patch_file('FileFormat')

        # FileReference
        if self.post_file_reference:
            self._post_patch_file('FileReference')

        # Workflow
        if self.post_workflow:
            self._post_patch_folder('Workflow')

        # Metaworkflow
        if self.post_metaworkflow:
            self._post_patch_folder('MetaWorkflow')

        # Workflow Descriptions
        if self.post_wfl:
            self._post_patch_wfl()

        # ECR
        if self.post_ecr:
            self._post_patch_ecr()


################################################
#  MAIN, runner
################################################
def main(args):
    """Deploy pipeline components from specified repositories to target environment.

    For each repository a PostPatchRepo object is created to:
        - Create and POST|PATCH to database objects in JSON format for
          Workflow, MetaWorkflow, FileReference, FileFormat, and Software components
        - PUSH workflow descriptions to target S3 bucket
        - BUILD Docker images and PUSH to target ECR folder
    """

    if not args.wfl_bucket:
        if args.post_workflow or args.post_wfl:
            error = 'MISSING ARGUMENT, --post-wfl | --post-workflow requires --wfl-bucket argument.\n'
            sys.exit(error)

    if not args.account:
        if args.post_workflow or args.post_wfl or args.post_ecr:
            error = 'MISSING ARGUMENT, --post-wfl | --post-workflow | --post-ecr requires --account argument.\n'
            sys.exit(error)

    if not args.region:
        if args.post_workflow or args.post_wfl or args.post_ecr:
            error = 'MISSING ARGUMENT, --post-wfl | --post-workflow | --post-ecr requires --region argument.\n'
            sys.exit(error)

    # Run
    for repo in args.repos:
        pprepo = PostPatchRepo(args, repo)
        pprepo.run_post_patch()

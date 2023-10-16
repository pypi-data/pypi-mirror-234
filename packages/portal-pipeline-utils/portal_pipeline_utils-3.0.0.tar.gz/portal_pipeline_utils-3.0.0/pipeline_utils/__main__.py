#!/usr/bin/env python3

################################################
#
#   __main__
#     this is the entry point for command line
#
#   Michele Berselli - berselli.michele@gmail.com
#
################################################


import sys, os
import argparse


# Commands
from pipeline_utils import pipeline_deploy


# Variables
PIPELINE_DEPLOY = 'pipeline_deploy'
CGAP_ALIAS = 'cgap-core'
DBMI_ALIAS = 'hms-dbmi'
KEYS_ALIAS = '~/.cgap-keys.json'
MAIN_ALIAS = 'main'
BUILDER_ALIAS = '<ff-env>-pipeline-builder'


# MAIN
def main(args=None):
    '''Command line wrapper around available commands.
    '''
    # Adding parser and subparsers
    parser = argparse.ArgumentParser(prog='pipeline_utils', description='Collection of utilities for deploying pipelines and interfacing with portal infrastructure')
    subparsers = parser.add_subparsers(dest='func', metavar="<command>")

    # Add pipeline_deploy to subparsers
    pipeline_deploy_parser = subparsers.add_parser(PIPELINE_DEPLOY, description='Utility to automatically deploy pipeline components from a target repository',
                                                    help='Utility to automatically deploy pipeline components from a target repository')

    pipeline_deploy_parser.add_argument('--ff-env', required=True, help='Environment to use for deployment')
    pipeline_deploy_parser.add_argument('--builder', required=False, help=f'Builder to use to deploy Docker containers to AWS ECR through AWS CodeBuild [{BUILDER_ALIAS}]')
    pipeline_deploy_parser.add_argument('--branch', required=False, help=f'Branch to use to deploy Docker containers to AWS ECR through AWS CodeBuild [{MAIN_ALIAS}]',
                                                        default=MAIN_ALIAS)
    pipeline_deploy_parser.add_argument('--local-build', action='store_true', help='Trigger a local build for Docker containers instead of using AWS CodeBuild')
    pipeline_deploy_parser.add_argument('--repos', required=True, nargs='+', help='List of directories for the repositories to deploy, each repository must follow the expected structure (see docs)')
    pipeline_deploy_parser.add_argument('--keydicts-json', required=False, help=f'Path to file with keys for portal auth in JSON format [{KEYS_ALIAS}]',
                                                           default=KEYS_ALIAS)
    pipeline_deploy_parser.add_argument('--wfl-bucket', required=False, help='Bucket to use for upload of Workflow Description files')
    pipeline_deploy_parser.add_argument('--account', required=False, help='AWS account to use for deployment')
    pipeline_deploy_parser.add_argument('--region', required=False, help='AWS account region to use for deployment')
    pipeline_deploy_parser.add_argument('--project', required=False, help=f'Project to use for deployment [{CGAP_ALIAS}]',
                                                          default=CGAP_ALIAS)
    pipeline_deploy_parser.add_argument('--institution', required=False, help=f'Institution to use for deployment [{DBMI_ALIAS}]',
                                                              default=DBMI_ALIAS)

    pipeline_deploy_parser.add_argument('--post-software', action='store_true', help='POST|PATCH Software objects')
    pipeline_deploy_parser.add_argument('--post-file-format', action='store_true', help='POST|PATCH FileFormat objects')
    pipeline_deploy_parser.add_argument('--post-file-reference', action='store_true', help='POST|PATCH FileReference objects')
    pipeline_deploy_parser.add_argument('--post-workflow', action='store_true', help='POST|PATCH Workflow objects')
    pipeline_deploy_parser.add_argument('--post-metaworkflow', action='store_true', help='POST|PATCH MetaWorkflow objects')
    pipeline_deploy_parser.add_argument('--post-wfl', action='store_true', help='Upload Workflow Description files (.cwl, .wdl)')
    pipeline_deploy_parser.add_argument('--post-ecr', action='store_true', help='Build Docker container images and push to AWS ECR. By default will use AWS CodeBuild unless --local-build flag is set')

    pipeline_deploy_parser.add_argument('--debug', action='store_true', help='Turn off POST|PATCH action')
    pipeline_deploy_parser.add_argument('--verbose', action='store_true', help='Print the JSON structure created for the objects')

    pipeline_deploy_parser.add_argument('--validate', action='store_true', help='Validate YAML objects against schemas. Turn off POST|PATCH action and ignore --verbose and --debug flags')

    # sentieon-specific
    pipeline_deploy_parser.add_argument('--sentieon-server', required=False, help='Address for Sentieon license server',
                                                             default=None)

    # Subparsers map
    subparser_map = {
                    PIPELINE_DEPLOY: pipeline_deploy_parser
                    }

    # Checking arguments
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    elif len(sys.argv) == 2:
        if sys.argv[1] in subparser_map:
            subparser_map[sys.argv[1]].print_help(sys.stderr)
            sys.exit(1)
        else:
            parser.print_help(sys.stderr)
            sys.exit(1)
    args = parser.parse_args()

    # Call the right tool
    if args.func == PIPELINE_DEPLOY:
        pipeline_deploy.main(args)


if __name__ == "__main__":
    main()

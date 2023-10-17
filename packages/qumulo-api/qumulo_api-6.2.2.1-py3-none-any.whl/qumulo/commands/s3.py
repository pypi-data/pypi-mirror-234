# Copyright (c) 2022 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import argparse

from dataclasses import asdict
from typing import Any, Dict, List, Sequence

import qumulo.lib.opts
import qumulo.rest.s3 as s3

from qumulo.lib.identity_util import Identity
from qumulo.lib.request import pretty_json
from qumulo.lib.util import tabulate
from qumulo.rest_client import RestClient


class GetSettingsCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_get_settings'
    SYNOPSIS = 'Get S3 server settings'

    @staticmethod
    def main(rest_client: RestClient, _args: argparse.Namespace) -> None:
        print(rest_client.s3.get_settings().to_json())


class ModifySettingsCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_modify_settings'
    SYNOPSIS = 'Modify S3 server settings'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        enable_group = parser.add_mutually_exclusive_group()
        enable_group.add_argument(
            '--disable',
            '-d',
            dest='enabled',
            help='Disable S3 server',
            action='store_false',
            default=None,
        )
        enable_group.add_argument(
            '--enable',
            '-e',
            dest='enabled',
            help='Enable S3 server',
            action='store_true',
            default=None,
        )
        parser.add_argument(
            '--base-path',
            dest='base_path',
            help=(
                'The directory which will be the parent of all buckets created without an'
                ' explicitly specified path.'
            ),
            required=False,
        )
        parser.add_argument(
            '--multipart-upload-expiry-interval',
            dest='multipart_upload_expiry_interval',
            help=(
                'If a multipart upload is not modified in this amount of time, it is considered'
                ' stale and may be cleaned up automatically. The duration must be in the format'
                ' <quantity><units> where <quantity> is a positive integer less than 100 and'
                ' <units> is one of [months, weeks, days, hours] (e.g. 5days). To disable'
                " automatic cleanup, specify 'never' for the duration."
            ),
            required=False,
            default=None,
        )
        secure_group = parser.add_mutually_exclusive_group()
        secure_group.add_argument(
            '--secure',
            dest='secure',
            help='Configure the S3 server to only accept HTTPS connections',
            action='store_true',
            default=None,
        )
        secure_group.add_argument(
            '--insecure',
            dest='secure',
            help='Configure the S3 server to only accept HTTP connections',
            action='store_false',
            default=None,
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        if (
            args.enabled is None
            and args.base_path is None
            and args.multipart_upload_expiry_interval is None
            and args.secure is None
        ):
            err_msg = (
                'At least one of the following arguments is required: [--disable, --enable,'
                ' --base-path, --multipart-upload-expiry-interval, --secure, --insecure]'
            )

            raise ValueError(err_msg)

        config = s3.ConfigPatch()

        if args.enabled is not None:
            config.enabled = args.enabled
        if args.base_path is not None:
            config.base_path = args.base_path
        if args.multipart_upload_expiry_interval is not None:
            config.multipart_upload_expiry_interval = args.multipart_upload_expiry_interval
        if args.secure is not None:
            config.secure = args.secure

        print(rest_client.s3.modify_settings(config).to_json())


def make_access_keys_table(
    keys: Sequence[s3.AccessKeyDescription], display_headers: bool = True
) -> str:
    headers = ['access_key_id', 'owner', 'creation_time'] if display_headers else None
    rows = []
    for key in keys:
        row = []
        row.append(key.access_key_id)
        row.append(str(Identity(key.owner)))
        row.append(key.creation_time)
        rows.append(row)
    return tabulate(rows, headers)


class ListAccessKeysCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_list_access_keys'
    SYNOPSIS = 'List S3 access keys'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--json', action='store_true', help='Output JSON instead of table.')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        def list_access_keys_tab(rest_client: RestClient) -> None:
            results = rest_client.s3.list_access_keys()
            print(make_access_keys_table(results.entries, True))
            while results.paging.next:
                results = rest_client.s3.list_access_keys(start_at=results.paging.next)
                print(make_access_keys_table(results.entries, False))

        def list_access_keys_json(rest_client: RestClient) -> None:
            def append_asdict(
                trg: List[Dict[str, Any]], src: Sequence[s3.AccessKeyDescription]
            ) -> None:
                for access_key in src:
                    trg.append(asdict(access_key))

            entries: List[Dict[str, Any]] = []
            response = rest_client.s3.list_access_keys()
            append_asdict(entries, response.entries)
            while response.paging.next is not None:
                response = rest_client.s3.list_access_keys(start_at=response.paging.next)
                append_asdict(entries, response.entries)

            print(pretty_json({'entries': entries}))

        if args.json:
            list_access_keys_json(rest_client)
        else:
            list_access_keys_tab(rest_client)


class CreateAccessKeyCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_create_access_key'
    SYNOPSIS = 'Create S3 access key'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        identity = parser.add_mutually_exclusive_group(required=True)
        identity.add_argument(
            'identifier',
            nargs='?',
            help=(
                'An auth_id, SID, or name optionally qualified with a domain prefix (e.g '
                '"local:name", "ad:name", "AD\\name") or an ID type (e.g. "auth_id:513", '
                '"SID:S-1-1-0"). Groups are not supported for access keys, must be a user.'
            ),
        )
        identity.add_argument('--auth-id', type=int, help='Auth ID of the qumulo user')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        client = rest_client

        if args.auth_id:
            identity = Identity({'auth_id': str(args.auth_id)})
        else:
            identity = Identity(args.identifier)

        print(pretty_json(asdict(client.s3.create_access_key(identity))))


class DeleteAccessKeyCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_delete_access_key'
    SYNOPSIS = 'Delete an S3 access key'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--id', type=str, help='The ID of the access key to be deleted', required=True
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        rest_client.s3.delete_access_key(args.id)


def make_buckets_table(buckets: Sequence[s3.BucketDescription]) -> str:
    headers = ['name', 'creation_time', 'path']
    rows = []
    for bucket in buckets:
        row = []
        row.append(bucket.name)
        row.append(bucket.creation_time)
        row.append(bucket.path)
        rows.append(row)
    return tabulate(rows, headers)


class ListBucketsCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_list_buckets'
    SYNOPSIS = 'List all S3 buckets'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--json', action='store_true', help='Output JSON instead of table')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        results = rest_client.s3.list_buckets()
        if args.json:
            print(pretty_json(asdict(results)))
        else:
            print(make_buckets_table(results.buckets))


class GetBucketCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_get_bucket'
    SYNOPSIS = 'Get details for an S3 bucket'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--name', help='The name of the bucket to retrieve', required=True)

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        results = rest_client.s3.list_buckets()
        for bucket in results.buckets:
            if bucket.name == args.name:
                print(pretty_json(asdict(bucket)))
                return
        print(f'"{args.name}" not found.')


class CreateBucketCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_add_bucket'
    SYNOPSIS = 'Create an S3 bucket'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--name', help='The name of the bucket to be created', required=True)
        parser.add_argument(
            '--fs-path',
            help=(
                'The absolute path to be used as the root of the bucket. The user must have'
                ' permissions to read the directory.'
            ),
            required=False,
        )
        parser.add_argument(
            '--create-fs-path',
            help=(
                'Creates the bucket root if it does not exist. '
                'The user must have permission to create the directory.'
            ),
            action='store_true',
            default=False,
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        if args.fs_path is None and args.create_fs_path:
            err_msg = '--create-fs-path can only be specified if --fs-path is provided.'
            raise ValueError(err_msg)

        results = rest_client.s3.create_bucket(
            name=args.name, path=args.fs_path, create_path=args.create_fs_path
        )
        print(pretty_json(asdict(results)))


class DeleteBucketCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_delete_bucket'
    SYNOPSIS = 'Delete an S3 bucket'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--name', help='The name of the bucket to be deleted', required=True)
        parser.add_argument(
            '--delete-root-dir',
            action='store_true',
            default=False,
            help=(
                'If set to true, the operation will only succeed if the bucket root directory is'
                ' empty, and the caller has the necessary permissions to unlink it. Otherwise, the'
                ' directory need not be empty.'
            ),
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        rest_client.s3.delete_bucket(name=args.name, delete_root_dir=args.delete_root_dir)


class ModifyBucketCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_modify_bucket'
    SYNOPSIS = 'Modify S3 bucket settings'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--name', help='The name of the bucket to be modified', required=True)
        anonymous_group = parser.add_mutually_exclusive_group()
        anonymous_group.add_argument(
            '--disable-anonymous-access',
            dest='anonymous_access_enabled',
            help='Disallows unsigned S3 requests; will be refused with 403 Forbidden.',
            action='store_false',
            default=None,
        )
        anonymous_group.add_argument(
            '--enable-anonymous-access',
            dest='anonymous_access_enabled',
            help='Allows unsigned S3 requests; will execute with GUEST privilege.',
            action='store_true',
            default=None,
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        if args.anonymous_access_enabled is None:
            err_msg = (
                'At least one of the following arguments is required: [--disable-anonymous-access,'
                ' --enable-anonymous-access]'
            )
            raise ValueError(err_msg)

        patch = s3.BucketPatch(anonymous_access_enabled=args.anonymous_access_enabled)
        results = rest_client.s3.modify_bucket(name=args.name, patch=patch)
        print(pretty_json(asdict(results)))


class ListUploadsCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_list_uploads'
    SYNOPSIS = (
        'List in-progress S3 uploads. This includes user initiated multi-part uploads, and system'
        ' initiated uploads that are used in PutObject and CopyObject actions.'
    )

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--bucket', help='The bucket for which uploads should be listed.', required=True
        )
        parser.add_argument(
            '--starts-with',
            help='Only output uploads for keys that start with the given string',
            required=False,
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        starts_with = args.starts_with

        def append_asdict(tgt: List[Dict[str, Any]], src: Sequence[s3.UploadDescription]) -> None:
            for upload in src:
                if starts_with and not upload.key.startswith(starts_with):
                    continue
                tgt.append(asdict(upload))

        uploads: List[Dict[str, Any]] = []

        response = rest_client.s3.list_uploads(bucket=args.bucket)
        append_asdict(uploads, response.uploads)
        while response.paging.next is not None:
            response = rest_client.s3.list_uploads(
                bucket=args.bucket, start_after=response.paging.next
            )
            append_asdict(uploads, response.uploads)

        print(pretty_json({'uploads': uploads}))


class AbortUploadCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_abort_upload'
    SYNOPSIS = (
        'Aborts an in-progress S3 upload. This can be applied to both user initiated multi-part'
        ' uploads, and system initiated uploads that are used in PutObject and CopyObject actions.'
    )

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--bucket', help='The bucket in which the upload was initiated.', required=True
        )
        parser.add_argument('--upload-id', help='The upload to abort.', required=True)

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        rest_client.s3.abort_upload(bucket=args.bucket, upload_id=args.upload_id)

import argparse


class ArgParser:
    @classmethod
    def parse(cls, args) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            prog='bbpp - BitBucket Pipelines Monitor',
            description='Monitor BitBucket Pipelines status, notifies on states changes using system notifications',
        )

        subparsers = parser.add_subparsers(help='options')
        parser.add_argument(
            '-r', '--repository', help='Repository regex to monitor pipelines'
        )
        config_parser = subparsers.add_parser(
            'config',
            help='Configure authentication file.\n'
            ' File will be stored at ~/.bbpp/bbpp.conf',
        )
        config_parser.add_argument(
            '-u',
            '--username',
            help='BitBucket username.\n'
            '( cog / Personal Bitbucket Settings / Account Settings / Bitbucket profile settings section / Username )',
            required=True,
        )
        config_parser.add_argument(
            '-p',
            '--password',
            help='BitBucket App password. \n '
            '( cog / Personal Bitbucket Settings / App passwords ). \n'
            'Need Repositories read and Pipelines Read privileges.',
            required=True,
        )
        config_parser.add_argument(
            '-w',
            '--workspace',
            help='Workspace where the repository is located',
            default='cioapps',
        )
        config_parser.add_argument(
            '-s',
            '--sound',
            help='Sound file to play when a pipeline changes state. Only available on macos',
            default='ping.wav',
        )

        return parser.parse_args(args)

import argparse
from lumipy.provider.provider_sets import provider_sets
import lumipy.provider as lp


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'action',
        choices=['setup', 'run'],
        help='The lumipy.providers action to run. Available actions are: [run/setup].\n'
             '"setup" sets up the python providers. This will install/update the dotnet tool and (optionally) copy '
             'your certs to the tool\'s directory.\n'
             '"run" will run a provider set specified with --set.'
    )

    # Setup args
    parser.add_argument(
        '--secrets',
        dest='secrets',
        default=None,
        help='Path to your secrets file to use during setup. Defaults to None if not specified. In this case it will '
             'fall back to finding credentials in the environment variables.'
    )
    parser.add_argument(
        '--token',
        dest='token',
        default=None,
        help='The personal access token to use during setup. Defaults to None if not specified. In this case it will '
             'fall back to finding credentials in the environment variables.'
    )
    parser.add_argument(
        '--api_url',
        dest='api_url',
        default=None,
        help='Luminesce API URL to use during setup along with your token. Defaults to None if not specified. In this '
             'case it will fall back to finding credentials in the environment variables.'
    )

    # Run args
    sets_str = ', '.join(f"'{s}'" for s in provider_sets.keys())
    parser.add_argument(
        '--set',
        dest='provider_set',
        default=None,
        help=f'Which set of providers to run. Available sets: {sets_str}'
    )
    parser.add_argument(
        '--user',
        dest='user',
        default=None,
        help='Routing for the providers. Can be a user ID, global, or i not specified will open a browser window for '
             'you to login.'
    )
    parser.add_argument(
        '--domain',
        dest='domain',
        default=None,
        help='Domain to run the provider in.'
    )
    parser.add_argument(
        '--port',
        dest='port',
        default=5001,
        help='The port to run the python providers\' api server at',
        type=int
    )
    parser.add_argument(
        '--fbn-run',
        dest='fbn_run',
        action='store_true',
        help='Whether to use the fbn k8s authentication when running on the FINBOURNE estate. '
    )
    parser.add_argument(
        '--dry-run',
        dest='dry_run',
        action='store_true',
        help='Whether to run just the python API for testing, and not to connect to luminesce.'
    )
    parser.add_argument(
        '--whitelist-me',
        dest='whitelist_me',
        action='store_true',
        help='Whether to add this machine name to the whitelist for running providers globally. '
             'It will be blocked by default.'
    )
    args = parser.parse_args()

    if args.action == 'setup':
        lp.setup(api_secrets_filename=args.secrets, token=args.token, api_url=args.api_url)

    if args.action == 'run':

        set_name = args.provider_set

        if set_name not in provider_sets.keys():
            set_names = ', '.join(sorted(provider_sets.keys()))
            raise ValueError(f'Unrecognised provider set: "{set_name}".\nSupported values are {set_names}')

        lp.ProviderManager(
            *provider_sets[set_name],
            user=args.user,
            domain=args.domain,
            port=args.port,
            dry_run=args.dry_run,
            whitelist_me=args.whitelist_me,
            _fbn_run=args.fbn_run
        ).run()

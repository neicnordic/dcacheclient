"""
   dcache admin client.
"""

import argparse
import argcomplete
import configparser
import contextlib
import functools
import pprint
import logging
import sys
import traceback
import os

from argcomplete import warn
from requests.packages.urllib3 import disable_warnings

from dcacheclient import client
from dcacheclient.sync import panoptes

ROOTLOGGER = logging.getLogger('')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)


def get_config():
    '''
    Multi-step search for the configuration file:

        1. Local directory.  ./.dcachecfg.

        2. User's home directory (~user/.dcachecfg).

        3. A standard system-wide directory (/etc/dcache/.dcachecfg).

        4. A place named by an environment variable (DCACHE_CONF).
    '''
    config = configparser.ConfigParser()
    for loc in os.curdir, os.path.expanduser("~"), "/etc/dcache", os.environ.get("DCACHE_CONF"):
        try:
            if loc:
                LOGGER.debug('Reading configuration from %s' % (os.path.join(loc, ".dcachecfg")))
                with open(os.path.join(loc, ".dcachecfg")) as source:
                    config.read_file(source)
                return config
        except IOError:
            pass
    return config


@contextlib.contextmanager
def get_client(args):
    '''
    get client utility.
    '''
    dcache = client.Client(
        url=args.url,
        username=args.username, password=args.password,
        certificate=args.certificate,
        private_key=args.private_key,
        x509_proxy=args.x509_proxy,
        no_check_certificate=args.no_check_certificate,
        ca_certificate=args.ca_certificate,
        ca_directory=args.ca_directory,
        timeout=args.timeout,
        oidc_agent_account=args.oidc_agent_account)
    try:
        yield dcache
    except Exception:
        raise
    finally:
        dcache.close()


def print_response(response):
    """
    Print response.
    """
    pprint.pprint(response)


def completer_exception(function):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except:
            warn("error")
            warn(str(traceback.print_exc()))
            raise
    return wrapper


@completer_exception
def path_completer(prefix, parsed_args, **kwparsed_args):
    """
    Completes the argument with a list of paths.
    """
    dcache = client.Client(
        url=parsed_args.url,
        username=parsed_args.username, password=parsed_args.password,
        certificate=parsed_args.certificate, private_key=parsed_args.private_key,
        x509_proxy=parsed_args.x509_proxy,
        no_check_certificate=parsed_args.no_check_certificate,
        ca_certificate=parsed_args.ca_certificate, ca_directory=parsed_args.ca_directory,
        timeout=parsed_args.timeout)
    path, filename = prefix.rsplit('/', 1)
    response = dcache.namespace.get_file_attributes(
        path=path,
        children=True)
    paths = []
    for child in response['children']:
        normpath = os.path.normpath(path + '/' + child['fileName'])
        if child["fileType"] == "DIR":
            normpath += '/'
        paths.append(normpath)
    return paths


@completer_exception
def pool_completer(prefix, parsed_args, **kwparsed_args):
    """
    Completes the argument with a list of pools.
    """
    dcache = client.Client(
        url=parsed_args.url,
        username=parsed_args.username, password=parsed_args.password,
        certificate=parsed_args.certificate, private_key=parsed_args.private_key,
        x509_proxy=parsed_args.x509_proxy,
        no_check_certificate=parsed_args.no_check_certificate,
        ca_certificate=parsed_args.ca_certificate, ca_directory=parsed_args.ca_directory,
        timeout=parsed_args.timeout)
    response = dcache.pools.get_pools()
    return [pool["name"] for pool in response]


@completer_exception
def pool_group_completer(prefix, parsed_args, **kwparsed_args):
    """
    Completes the argument with a list of pool groups.
    """
    dcache = client.Client(
        url=parsed_args.url,
        username=parsed_args.username, password=parsed_args.password,
        certificate=parsed_args.certificate, private_key=parsed_args.private_key,
        x509_proxy=parsed_args.x509_proxy,
        no_check_certificate=parsed_args.no_check_certificate,
        ca_certificate=parsed_args.ca_certificate, ca_directory=parsed_args.ca_directory,
        timeout=parsed_args.timeout)
    response = dcache.poolmanager.get_pool_groups()
    return [pool_group["name"] for pool_group in response]


@completer_exception
def cell_address_completer(prefix, parsed_args, **kwparsed_args):
    """
    Completes the argument with a list of cell addresses.
    """
    dcache = client.Client(
        url=parsed_args.url,
        username=parsed_args.username, password=parsed_args.password,
        certificate=parsed_args.certificate, private_key=parsed_args.private_key,
        x509_proxy=parsed_args.x509_proxy,
        no_check_certificate=parsed_args.no_check_certificate,
        ca_certificate=parsed_args.ca_certificate, ca_directory=parsed_args.ca_directory,
        timeout=parsed_args.timeout)
    response = dcache.cells.get_addresses()
    return [cell_address for cell_address in response]


def qos_get_qos_list(args):
    """
    List the available quality of services for a specific object type.  Requires authentication.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.qos.get_qos_list(**vars(args))
        print_response(response)


def qos_get_queried_qos_for_files(args):
    """
    Provide information about a specific file quality of services.  Requires authentication.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.qos.get_queried_qos_for_files(**vars(args))
        print_response(response)


def qos_get_queried_qos_for_directories(args):
    """
    Provides information about a specific directory quality of services.  Requires authentication.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.qos.get_queried_qos_for_directories(**vars(args))
        print_response(response)


def events_channel_metadata(args):
    """
    Obtain metadata about a channel.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.events.channel_metadata(**vars(args))
        print_response(response)


def events_delete_channel(args):
    """
    Cancel a channel.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.events.delete_channel(**vars(args))
        print_response(response)


def events_modify(args):
    """
    Modify a channel.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.events.modify(**vars(args))
        print_response(response)


def events_get_channels(args):
    """
    Obtain a list of channels.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.events.get_channels(**vars(args))
        print_response(response)


def events_register(args):
    """
    Request a new channel.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.events.register(**vars(args))
        print_response(response)


def events_channel_subscription(args):
    """
    Return the selector of this subscription.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.events.channel_subscription(**vars(args))
        print_response(response)


def events_delete(args):
    """
    Cancel a subscription.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.events.delete(**vars(args))
        print_response(response)


def events_subscribe(args):
    """
    Subscribe to events.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.events.subscribe(**vars(args))
        print_response(response)


def events_channel_subscriptions(args):
    """
    Obtain list a channel's subscriptions.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.events.channel_subscriptions(**vars(args))
        print_response(response)


def events_get_event_types(args):
    """
    Obtain a list of the available event types.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.events.get_event_types(**vars(args))
        print_response(response)


def events_get_selector_schema(args):
    """
    Obtain the JSON schema for this event type's selectors.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.events.get_selector_schema(**vars(args))
        print_response(response)


def events_get_event_schema(args):
    """
    Obtain the JSON schema for events of this event type.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.events.get_event_schema(**vars(args))
        print_response(response)


def events_service_metadata(args):
    """
    Obtain general information about event support in dCache.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.events.service_metadata(**vars(args))
        print_response(response)


def events_get_event_type(args):
    """
    Obtain non-schema information about a specific event type.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.events.get_event_type(**vars(args))
        print_response(response)


def alarms_get_priority(args):
    """
    Request the current mapping of an alarm type to its priority. Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.alarms.get_priority(**vars(args))
        print_response(response)


def alarms_get_alarms(args):
    """
    Provides a filtered list of log entries. Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.alarms.get_alarms(**vars(args))
        print_response(response)


def alarms_bulk_update_or_delete(args):
    """
    Batch request to update or delete the indicated alarms. Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.alarms.bulk_update_or_delete(**vars(args))
        print_response(response)


def alarms_delete_alarm_entry(args):
    """
    Delete a specific log entry. Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.alarms.delete_alarm_entry(**vars(args))
        print_response(response)


def alarms_update_alarm_entry(args):
    """
    Request to open or close the indicated log entry. Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.alarms.update_alarm_entry(**vars(args))
        print_response(response)


def alarms_get_priorities(args):
    """
    Request the current mapping of all alarm types to priorities. Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.alarms.get_priorities(**vars(args))
        print_response(response)


def billing_get_data(args):
    """
    Request the time series data for a particular specification. The available specifications can be obtained via GET on histograms/grid/description.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.billing.get_data(**vars(args))
        print_response(response)


def billing_get_p2ps(args):
    """
    Provides a list of pool-to-pool transfers for a specific PNFS-ID.  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.billing.get_p2ps(**vars(args))
        print_response(response)


def billing_get_reads(args):
    """
    Provides a list of read transfers for a specific PNFS-ID.  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.billing.get_reads(**vars(args))
        print_response(response)


def billing_get_restores(args):
    """
    Provide a list of tape reads for a specific PNFS-ID.  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.billing.get_restores(**vars(args))
        print_response(response)


def billing_get_stores(args):
    """
    Provides a list of tape writes for a specific PNFS-ID.  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.billing.get_stores(**vars(args))
        print_response(response)


def billing_get_writes(args):
    """
    Provides a list of write transfers for a specific PNFS-ID.  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.billing.get_writes(**vars(args))
        print_response(response)


def billing_get_grid(args):
    """
    Provides the list of available histograms with their corresponding identifer.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.billing.get_grid(**vars(args))
        print_response(response)


def billing_get_grid_data(args):
    """
    Provide the full "grid" of time series data in one pass. Data is sorted lexicographically by key.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.billing.get_grid_data(**vars(args))
        print_response(response)


def cells_get_cells(args):
    """
    Provide information about all cells.  Requires admin role. Results sorted lexicographically by cell name.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.cells.get_cells(**vars(args))
        print_response(response)


def cells_get_cell_data(args):
    """
    Provide information about a specific cell.  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.cells.get_cell_data(**vars(args))
        print_response(response)


def cells_get_addresses(args):
    """
    Get a list of current addresses for well-known cells.  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.cells.get_addresses(**vars(args))
        print_response(response)


def identity_get_user_attributes(args):
    """
    Provide information about the current user.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.identity.get_user_attributes(**vars(args))
        print_response(response)


def namespace_get_file_attributes(args):
    """
    Find metadata and optionally directory contents.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.namespace.get_file_attributes(**vars(args))
        print_response(response)


def namespace_cmr_resources(args):
    """
    Modify a file or directory.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.namespace.cmr_resources(**vars(args))
        print_response(response)


def namespace_delete_file_entry(args):
    """
    delete a file or directory
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.namespace.delete_file_entry(**vars(args))
        print_response(response)


def namespace_get_attributes(args):
    """
    Discover information about a file from the PNFS-ID.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.namespace.get_attributes(**vars(args))
        print_response(response)


def poolmanager_get_pool_groups(args):
    """
    Get a list of poolgroups.  Requires admin role. Results sorted lexicographically by group name.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.poolmanager.get_pool_groups(**vars(args))
        print_response(response)


def poolmanager_get_pool_group(args):
    """
    Get information about a poolgroup.  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.poolmanager.get_pool_group(**vars(args))
        print_response(response)


def poolmanager_get_pools_of_group(args):
    """
    Get a list of pools that are a member of a poolgroup.  If no poolgroup is specified then all pools are listed. Results sorted lexicographically by pool name.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.poolmanager.get_pools_of_group(**vars(args))
        print_response(response)


def poolmanager_get_group_usage(args):
    """
    Get usage metadata about a specific poolgroup.  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.poolmanager.get_group_usage(**vars(args))
        print_response(response)


def poolmanager_get_queue_info(args):
    """
    Get pool activity information about pools of a specific poolgroup.  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.poolmanager.get_queue_info(**vars(args))
        print_response(response)


def poolmanager_get_space_info(args):
    """
    Get space information about pools of a specific poolgroup.  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.poolmanager.get_space_info(**vars(args))
        print_response(response)


def poolmanager_get_queue_histograms(args):
    """
    Get aggregated pool activity histogram information from pools in a specific poolgroup.  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.poolmanager.get_queue_histograms(**vars(args))
        print_response(response)


def poolmanager_get_files_histograms(args):
    """
    Get aggregated file statistics histogram information from pools in a specific poolgroup.  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.poolmanager.get_files_histograms(**vars(args))
        print_response(response)


def pools_get_pool(args):
    """
    Get information about a specific pool (name, group membership, links). Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.pools.get_pool(**vars(args))
        print_response(response)


def pools_get_movers(args):
    """
    Get mover information for a specific pool.  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.pools.get_movers(**vars(args))
        print_response(response)


def pools_get_queue_histograms(args):
    """
    Get histogram data concerning activity on a specific pool (48-hour window).
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.pools.get_queue_histograms(**vars(args))
        print_response(response)


def pools_get_files_histograms(args):
    """
    Get histogram data concerning file lifetime on a specific pool (60-day window).
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.pools.get_files_histograms(**vars(args))
        print_response(response)


def pools_get_pool_usage(args):
    """
    Get information about a specific pool (configuration, state, usage).  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.pools.get_pool_usage(**vars(args))
        print_response(response)


def pools_get_repository_info_for_file(args):
    """
    Get information about a specific PNFS-ID usage within a specific pool.  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.pools.get_repository_info_for_file(**vars(args))
        print_response(response)


def pools_get_nearline_queues(args):
    """
    Get nearline activity information for a specific pool.  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.pools.get_nearline_queues(**vars(args))
        print_response(response)


def pools_kill_movers(args):
    """
    Kill a mover.  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.pools.kill_movers(**vars(args))
        print_response(response)


def pools_update_mode(args):
    """
    Modify a pool's mode.  Requires admin role.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.pools.update_mode(**vars(args))
        print_response(response)


def pools_get_pools(args):
    """
    Get information about all pools (name, group membership, links).  Requires admin role.  Results sorted lexicographically by pool name.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.pools.get_pools(**vars(args))
        print_response(response)


def pools_get_restores(args):
    """
    Obtain a (potentially partial) list of restore operations from some snapshot, along with a token that identifies the snapshot.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.pools.get_restores(**vars(args))
        print_response(response)


def poolmanager_get_links(args):
    """
    Get information about all links.  Requires admin role. Results sorted lexicographically by link name.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.poolmanager.get_links(**vars(args))
        print_response(response)


def poolmanager_get_link_groups(args):
    """
    Get information about all linkgroups.  Requires admin role. Results sorted lexicographically by link group name.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.poolmanager.get_link_groups(**vars(args))
        print_response(response)


def poolmanager_get_partitions(args):
    """
    Get information about all partitions.  Requires admin role. Results sorted lexicographically by partition name.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.poolmanager.get_partitions(**vars(args))
        print_response(response)


def poolmanager_match(args):
    """
    Describe the pools selected by a particular request.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.poolmanager.match(**vars(args))
        print_response(response)


def poolmanager_get_units(args):
    """
    List all units.  Requires admin role. Results sorted lexicographically by unit name.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.poolmanager.get_units(**vars(args))
        print_response(response)


def poolmanager_get_unit_groups(args):
    """
    List all unitgroups.  Requires admin role. Results sorted lexicographically by unit group name.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.poolmanager.get_unit_groups(**vars(args))
        print_response(response)


def spacemanager_get_tokens_for_group(args):
    """
    Get information about space tokens.  Requires admin role.  Results sorted by token id.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.spacemanager.get_tokens_for_group(**vars(args))
        print_response(response)


def spacemanager_get_link_groups(args):
    """
    Get information about link groups.  Requires admin role. Results sorted lexicographically by link group name.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.spacemanager.get_link_groups(**vars(args))
        print_response(response)


def transfers_get_transfers(args):
    """
    Provide a list of all client-initiated transfers that are either queued or currently running.  Internal (pool-to-pool) transfers are excluded.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.transfers.get_transfers(**vars(args))
        print_response(response)


def bring_online(args):
    """
    Bring online a file.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = dcache.namespace.bring_online(path=args.path)
        print_response(response)


def sync_storage(args):
    """
    Synchronise storage.
    """
    LOGGER.debug('args: %s' % str(args))
    with get_client(args) as dcache:
        response = panoptes.main(
            root_path=args.root_path,
            source=args.source,
            destination=args.destination,
            client=dcache,
            fts_host=args.fts_host,
            recursive=args.recursive)
        print_response(response)


def complete(args):
    """
    Print bash completion command.
    """
    # print ('eval "$(register-python-argcomplete my-favorite-script.py)"')
    print(argcomplete.shellcode('dcache-admin'))


def get_parser(config):
    '''
    Get parser.
    '''
    oparser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]),
        add_help=True)
    oparser.add_argument(
        '--debug',
        '-d',
        action='store_true',
        help='print debug messages to stderr.')
    oparser.add_argument(
        '--url', dest="url",
        help="The service url.",
        default=config.get('default', 'url', fallback='https://localhost:3880'))

    oparser.add_argument(
        '-t', '--timeout', dest='timeout',
        action="store", type=int,
        default=config.get('default', 'timeout', fallback=None),
        help='Timeout in seconds.')

    # Options for userpass
    oparser.add_argument(
        '-u', '--user', dest='username',
        default=config.get('default', 'username', fallback=None),
        help='username.')
    oparser.add_argument(
        '-pwd', '--password', dest='password',
        default=config.get('default', 'password', fallback=None),
        help='password.')

    # Options for server certificate
    oparser.add_argument(
        '--ca-certificate',
        dest='ca_certificate',
        default=None,
        help='CA certificate to verify peer against (SSL).')
    oparser.add_argument(
        '--ca-directory', dest='ca_directory', default='/etc/grid-security/certificates/',
        help='CA directory to verify peer against (SSL).')
    oparser.add_argument(
        '--no-check-certificate', dest='no_check_certificate',
        action='store_true',
        help="Don't validate the server's certificate.")

    # Options for x509 certificate
    oparser.add_argument(
        '--certificate',
        dest='certificate',
        default=config.get('default', 'certificate', fallback=None),
        help='Client certificate file.')
    oparser.add_argument(
        '--private-key',
        dest='private_key',
        default=config.get('default', 'key', fallback=None),
        help='Private key file.')

    # Options for X.509 grid proxy
    oparser.add_argument(
        '--x509_proxy', dest='x509_proxy',
        nargs='?', const=os.environ.get('X509_USER_PROXY', '/tmp/x509up_u' + str(os.getuid())),
        help='Client X509 proxy file.')

    # Options for OIDC
    oparser.add_argument(
        '--oidc-agent-account',
        metavar="ACCOUNT",
        dest='oidc_agent_account',
        default=config.get('default', 'oidc-agent-account', fallback=None),
        help='The name of the oidc-agent account to use when authenticating with dCache')


    oparser.set_defaults(func=oparser.print_help)
    subparsers = oparser.add_subparsers()

    # The complete subparser
    complete_parser = subparsers.add_parser(
        'complete',
        help='print bash completion command',
        add_help=True)
    complete_parser.set_defaults(func=complete)

    # The alarms subparser
    alarms_parser = subparsers.add_parser(
        'alarms',
        help='The log of internal problems',
        add_help=True)
    alarms_parser.set_defaults(func=alarms_parser.print_help)
    alarms_subparser = alarms_parser.add_subparsers()

    # getPriority subparser
    getPriority_parser = alarms_subparser.add_parser(
        'getPriority',
        help="""Request the current mapping of an alarm type to its priority. Requires admin role.""")
    getPriority_parser.set_defaults(func=alarms_get_priority)
    getPriority_parser.add_argument('--type', required=True, help="""The alarm type.""", action='store')

    # getAlarms subparser
    getAlarms_parser = alarms_subparser.add_parser(
        'getAlarms',
        help="""Provides a filtered list of log entries. Requires admin role.""")
    getAlarms_parser.set_defaults(func=alarms_get_alarms)
    getAlarms_parser.add_argument('--offset', required=False, help="""Number of entries to skip in directory listing.""", type=int)
    getAlarms_parser.add_argument('--limit', required=False, help="""Limit number of replies in directory listing.""", type=int)
    getAlarms_parser.add_argument('--after', required=False, help="""Return no alarms before this datestamp, in unix-time.""", type=int)
    getAlarms_parser.add_argument('--before', required=False, help="""Return no alarms after this datestamp, in unix-time.""", type=int)
    getAlarms_parser.add_argument('--includeClosed', required=False, help="""Whether to include closed alarms.""", action='store_true')
    getAlarms_parser.add_argument('--severity', required=False, help="""Select log entries with at least this severity.""", action='store')
    getAlarms_parser.add_argument('--type', required=False, help="""Select only log entries of this alarm type.""", action='store')
    getAlarms_parser.add_argument('--host', required=False, help="""Select only log entries from this host.""", action='store')
    getAlarms_parser.add_argument('--domain', required=False, help="""Select only log entries from this domain.""", action='store')
    getAlarms_parser.add_argument('--service', required=False, help="""Select only log entries from this service.""", action='store')
    getAlarms_parser.add_argument('--info', required=False, help="""Select only log entries that match the info.""", action='store')
    getAlarms_parser.add_argument('--sort', required=False, help="""A comma-seperated list of fields to sort log entries.""", action='store')

    # bulkUpdateOrDelete subparser
    bulkUpdateOrDelete_parser = alarms_subparser.add_parser(
        'bulkUpdateOrDelete',
        help="""Batch request to update or delete the indicated alarms. Requires admin role.""")
    bulkUpdateOrDelete_parser.set_defaults(func=alarms_bulk_update_or_delete)
    bulkUpdateOrDelete_parser.add_argument('--body', required=False, help="""A JSON object describing the changes.  The "action" item is a string with either "update" or "delete" as a value.  The "items" item is a JSON Array. For the "delete" action, this array contains strings, each the key of a log entry to delete.  For the "update" action, the array contains JSON objects with a "key" item and a "closed" item.  The closed value is a boolean and the key value is a String.""", action='store')

    # deleteAlarmEntry subparser
    deleteAlarmEntry_parser = alarms_subparser.add_parser(
        'deleteAlarmEntry',
        help="""Delete a specific log entry. Requires admin role.""")
    deleteAlarmEntry_parser.set_defaults(func=alarms_delete_alarm_entry)
    deleteAlarmEntry_parser.add_argument('--key', required=True, help="""The identifier for the specific log entry.""", action='store')

    # updateAlarmEntry subparser
    updateAlarmEntry_parser = alarms_subparser.add_parser(
        'updateAlarmEntry',
        help="""Request to open or close the indicated log entry. Requires admin role.""")
    updateAlarmEntry_parser.set_defaults(func=alarms_update_alarm_entry)
    updateAlarmEntry_parser.add_argument('--key', required=True, help="""The identifier for the specific log entry.""", action='store')
    updateAlarmEntry_parser.add_argument('--body', required=False, help="""A JSON Object with a 'closed' item containing a JSON Boolean value.""", action='store')

    # getPriorities subparser
    getPriorities_parser = alarms_subparser.add_parser(
        'getPriorities',
        help="""Request the current mapping of all alarm types to priorities. Requires admin role.""")
    getPriorities_parser.set_defaults(func=alarms_get_priorities)
    # The billing subparser
    billing_parser = subparsers.add_parser(
        'billing',
        help='The log of (significant) client activity',
        add_help=True)
    billing_parser.set_defaults(func=billing_parser.print_help)
    billing_subparser = billing_parser.add_subparsers()

    # getData subparser
    getData_parser = billing_subparser.add_parser(
        'getData',
        help="""Request the time series data for a particular specification. The available specifications can be obtained via GET on histograms/grid/description.""")
    getData_parser.set_defaults(func=billing_get_data)
    getData_parser.add_argument('--key', required=True, help="""The specification identifier for which to fetch data.""", action='store')

    # getP2ps subparser
    getP2ps_parser = billing_subparser.add_parser(
        'getP2ps',
        help="""Provides a list of pool-to-pool transfers for a specific PNFS-ID.  Requires admin role.""")
    getP2ps_parser.set_defaults(func=billing_get_p2ps)
    getP2ps_parser.add_argument('--pnfsid', required=True, help="""The file to list.""", action='store')
    getP2ps_parser.add_argument('--before', required=False, help="""Return no transfers after this datestamp.""", action='store')
    getP2ps_parser.add_argument('--after', required=False, help="""Return no transfers before this datestamp.""", action='store')
    getP2ps_parser.add_argument('--limit', required=False, help="""Maximum number of transfers to return.""", type=int)
    getP2ps_parser.add_argument('--offset', required=False, help="""Number of transfers to skip.""", type=int)
    getP2ps_parser.add_argument('--serverPool', required=False, help="""Only select transfers from the specified pool.""", action='store')
    getP2ps_parser.add_argument('--clientPool', required=False, help="""Only select transfers to the specified pool.""", action='store')
    getP2ps_parser.add_argument('--client', required=False, help="""Only select transfers triggered by the specified client.""", action='store')
    getP2ps_parser.add_argument('--sort', required=False, help="""How to sort responses.""", default='date', action='store')

    # getReads subparser
    getReads_parser = billing_subparser.add_parser(
        'getReads',
        help="""Provides a list of read transfers for a specific PNFS-ID.  Requires admin role.""")
    getReads_parser.set_defaults(func=billing_get_reads)
    getReads_parser.add_argument('--pnfsid', required=True, help="""The file to list.""", action='store')
    getReads_parser.add_argument('--before', required=False, help="""Return no reads after this datestamp.""", action='store')
    getReads_parser.add_argument('--after', required=False, help="""Return no reads before this datestamp.""", action='store')
    getReads_parser.add_argument('--limit', required=False, help="""Maximum number of reads to return.""", type=int)
    getReads_parser.add_argument('--offset', required=False, help="""Number of reads to skip.""", type=int)
    getReads_parser.add_argument('--pool', required=False, help="""Only select reads from the specified pool.""", action='store').completer = pool_completer
    getReads_parser.add_argument('--door', required=False, help="""Only select reads initiated by the specified door.""", action='store')
    getReads_parser.add_argument('--client', required=False, help="""Only select reads requested by the client.""", action='store')
    getReads_parser.add_argument('--sort', required=False, help="""How to sort responses.""", default='date', action='store')

    # getRestores subparser
    getRestores_parser = billing_subparser.add_parser(
        'getRestores',
        help="""Provide a list of tape reads for a specific PNFS-ID.  Requires admin role.""")
    getRestores_parser.set_defaults(func=billing_get_restores)
    getRestores_parser.add_argument('--pnfsid', required=True, help="""The file to list.""", action='store')
    getRestores_parser.add_argument('--before', required=False, help="""Return no tape reads after this datestamp.""", action='store')
    getRestores_parser.add_argument('--after', required=False, help="""Return no tape reads before this datestamp.""", action='store')
    getRestores_parser.add_argument('--limit', required=False, help="""Maximum number of tape reads to return.""", type=int)
    getRestores_parser.add_argument('--offset', required=False, help="""Number of tape reads to skip.""", type=int)
    getRestores_parser.add_argument('--pool', required=False, help="""Only select tape reads involving the specified pool.""", action='store').completer = pool_completer
    getRestores_parser.add_argument('--sort', required=False, help="""How to sort responses.""", default='date', action='store')

    # getStores subparser
    getStores_parser = billing_subparser.add_parser(
        'getStores',
        help="""Provides a list of tape writes for a specific PNFS-ID.  Requires admin role.""")
    getStores_parser.set_defaults(func=billing_get_stores)
    getStores_parser.add_argument('--pnfsid', required=True, help="""The file to list.""", action='store')
    getStores_parser.add_argument('--before', required=False, help="""Return no tape writes after this datestamp.""", action='store')
    getStores_parser.add_argument('--after', required=False, help="""Return no tape writes before this datestamp.""", action='store')
    getStores_parser.add_argument('--limit', required=False, help="""Maximum number of tape writes to return.""", type=int)
    getStores_parser.add_argument('--offset', required=False, help="""Number of tape writes to skip.""", type=int)
    getStores_parser.add_argument('--pool', required=False, help="""Only select tape writes involving the specified pool.""", action='store').completer = pool_completer
    getStores_parser.add_argument('--sort', required=False, help="""How to sort responses.""", default='date', action='store')

    # getWrites subparser
    getWrites_parser = billing_subparser.add_parser(
        'getWrites',
        help="""Provides a list of write transfers for a specific PNFS-ID.  Requires admin role.""")
    getWrites_parser.set_defaults(func=billing_get_writes)
    getWrites_parser.add_argument('--pnfsid', required=True, help="""The file to list.""", action='store')
    getWrites_parser.add_argument('--before', required=False, help="""Return no writes after this datestamp.""", action='store')
    getWrites_parser.add_argument('--after', required=False, help="""Return no writes before this datestamp.""", action='store')
    getWrites_parser.add_argument('--limit', required=False, help="""Maximum number of writes to return.""", type=int)
    getWrites_parser.add_argument('--offset', required=False, help="""Number of writes to skip.""", type=int)
    getWrites_parser.add_argument('--pool', required=False, help="""Only select writes from the specified pool.""", action='store').completer = pool_completer
    getWrites_parser.add_argument('--door', required=False, help="""Only select writes initiated by the specified door.""", action='store')
    getWrites_parser.add_argument('--client', required=False, help="""Only select writes requested by the client.""", action='store')
    getWrites_parser.add_argument('--sort', required=False, help="""How to sort responses.""", default='date', action='store')

    # getGrid subparser
    getGrid_parser = billing_subparser.add_parser(
        'getGrid',
        help="""Provides the list of available histograms with their corresponding identifer.""")
    getGrid_parser.set_defaults(func=billing_get_grid)

    # getGridData subparser
    getGridData_parser = billing_subparser.add_parser(
        'getGridData',
        help="""Provide the full "grid" of time series data in one pass. Data is sorted lexicographically by key.""")
    getGridData_parser.set_defaults(func=billing_get_grid_data)
    # The cells subparser
    cells_parser = subparsers.add_parser(
        'cells',
        help='The running components within dCache',
        add_help=True)
    cells_parser.set_defaults(func=cells_parser.print_help)
    cells_subparser = cells_parser.add_subparsers()

    # getCells subparser
    getCells_parser = cells_subparser.add_parser(
        'getCells',
        help="""Provide information about all cells.  Requires admin role. Results sorted lexicographically by cell name.""")
    getCells_parser.set_defaults(func=cells_get_cells)

    # getCellData subparser
    getCellData_parser = cells_subparser.add_parser(
        'getCellData',
        help="""Provide information about a specific cell.  Requires admin role.""")
    getCellData_parser.set_defaults(func=cells_get_cell_data)
    getCellData_parser.add_argument('--address', required=True, help="""The cell to query""", action='store').completer = cell_address_completer

    # getAddresses subparser
    getAddresses_parser = cells_subparser.add_parser(
        'getAddresses',
        help="""Get a list of current addresses for well-known cells.  Requires admin role.""")
    getAddresses_parser.set_defaults(func=cells_get_addresses)
    # The identity subparser
    identity_parser = subparsers.add_parser(
        'identity',
        help='Information about users',
        add_help=True)
    identity_parser.set_defaults(func=identity_parser.print_help)
    identity_subparser = identity_parser.add_subparsers()

    # getUserAttributes subparser
    getUserAttributes_parser = identity_subparser.add_parser(
        'getUserAttributes',
        help="""Provide information about the current user.""")
    getUserAttributes_parser.set_defaults(func=identity_get_user_attributes)
    # The namespace subparser
    namespace_parser = subparsers.add_parser(
        'namespace',
        help='Files, directories and similar objects',
        add_help=True)
    namespace_parser.set_defaults(func=namespace_parser.print_help)
    namespace_subparser = namespace_parser.add_subparsers()

    # getFileAttributes subparser
    getFileAttributes_parser = namespace_subparser.add_parser(
        'getFileAttributes',
        help="""Find metadata and optionally directory contents.""")
    getFileAttributes_parser.set_defaults(func=namespace_get_file_attributes)
    getFileAttributes_parser.add_argument('--path', required=True, help="""Path of file or directory.""", action='store').completer = path_completer
    getFileAttributes_parser.add_argument('--children', required=False, help="""Whether to include directory listing.""", action='store_true')
    getFileAttributes_parser.add_argument('--locality', required=False, help="""Whether to include file locality information.""", action='store_true')
    getFileAttributes_parser.add_argument('--locations', required=False, help="""Whether to include replica locations.""", action='store_true')
    getFileAttributes_parser.add_argument('--qos', required=False, help="""Whether to include quality of service.""", action='store_true')
    getFileAttributes_parser.add_argument('--limit', required=False, help="""Limit number of replies in directory listing.""", action='store')
    getFileAttributes_parser.add_argument('--offset', required=False, help="""Number of entries to skip in directory listing.""", action='store')

    # cmrResources subparser
    cmrResources_parser = namespace_subparser.add_parser(
        'cmrResources',
        help="""Modify a file or directory.""")
    cmrResources_parser.set_defaults(func=namespace_cmr_resources)
    cmrResources_parser.add_argument('--path', required=True, help="""Path of file or directory to be modified.""", action='store').completer = path_completer
    cmrResources_parser.add_argument('--body', required=True, help="""A JSON object that has an 'action' item with a String value.
If the 'action' value is 'mkdir' then a new directory is created with the name taken from the value of the JSON object 'name' item.  This directory is created within the supplied path parameter, which must be an existing directory.
If action is 'mv' then the file or directory specified by the path parameter is moved and/or renamed with the value of the JSON object 'destination' item describing the final location.  If the 'destination' value is a relative path then it is resolved against the path parameter value.
If action is 'qos' then the value of the JSON object 'target' item describes the desired QoS.""", action='store')

    # deleteFileEntry subparser
    deleteFileEntry_parser = namespace_subparser.add_parser(
        'deleteFileEntry',
        help="""delete a file or directory""")
    deleteFileEntry_parser.set_defaults(func=namespace_delete_file_entry)
    deleteFileEntry_parser.add_argument('--path', required=True, help="""Path of file or directory.""", action='store').completer = path_completer

    # getAttributes subparser
    getAttributes_parser = namespace_subparser.add_parser(
        'getAttributes',
        help="""Discover information about a file from the PNFS-ID.""")
    getAttributes_parser.set_defaults(func=namespace_get_attributes)
    getAttributes_parser.add_argument('--pnfsid', required=True, help="""The PNFS-ID of a file or directory.""", action='store')
    # The poolmanager subparser
    poolmanager_parser = subparsers.add_parser(
        'poolmanager',
        help='Data placement and selection decisions',
        add_help=True)
    poolmanager_parser.set_defaults(func=poolmanager_parser.print_help)
    poolmanager_subparser = poolmanager_parser.add_subparsers()

    # getPoolGroups subparser
    getPoolGroups_parser = poolmanager_subparser.add_parser(
        'getPoolGroups',
        help="""Get a list of poolgroups.  Requires admin role. Results sorted lexicographically by group name.""")
    getPoolGroups_parser.set_defaults(func=poolmanager_get_pool_groups)

    # getPoolGroup subparser
    getPoolGroup_parser = poolmanager_subparser.add_parser(
        'getPoolGroup',
        help="""Get information about a poolgroup.  Requires admin role.""")
    getPoolGroup_parser.set_defaults(func=poolmanager_get_pool_group)
    getPoolGroup_parser.add_argument('--group', required=True, help="""The poolgroup to be described.""", action='store').completer = pool_group_completer

    # getPoolsOfGroup subparser
    getPoolsOfGroup_parser = poolmanager_subparser.add_parser(
        'getPoolsOfGroup',
        help="""Get a list of pools that are a member of a poolgroup.  If no poolgroup is specified then all pools are listed. Results sorted lexicographically by pool name.""")
    getPoolsOfGroup_parser.set_defaults(func=poolmanager_get_pools_of_group)
    getPoolsOfGroup_parser.add_argument('--group', required=True, help="""The poolgroup to be described.""", action='store').completer = pool_group_completer

    # getGroupUsage subparser
    getGroupUsage_parser = poolmanager_subparser.add_parser(
        'getGroupUsage',
        help="""Get usage metadata about a specific poolgroup.  Requires admin role.""")
    getGroupUsage_parser.set_defaults(func=poolmanager_get_group_usage)
    getGroupUsage_parser.add_argument('--group', required=True, help="""The poolgroup to be described.""", action='store').completer = pool_group_completer

    # getQueueInfo subparser
    getQueueInfo_parser = poolmanager_subparser.add_parser(
        'getQueueInfo',
        help="""Get pool activity information about pools of a specific poolgroup.  Requires admin role.""")
    getQueueInfo_parser.set_defaults(func=poolmanager_get_queue_info)
    getQueueInfo_parser.add_argument('--group', required=True, help="""The poolgroup to be described.""", action='store').completer = pool_group_completer

    # getSpaceInfo subparser
    getSpaceInfo_parser = poolmanager_subparser.add_parser(
        'getSpaceInfo',
        help="""Get space information about pools of a specific poolgroup.  Requires admin role.""")
    getSpaceInfo_parser.set_defaults(func=poolmanager_get_space_info)
    getSpaceInfo_parser.add_argument('--group', required=True, help="""The poolgroup to be described.""", action='store').completer = pool_group_completer

    # getQueueHistograms subparser
    getQueueHistograms_parser = poolmanager_subparser.add_parser(
        'getQueueHistograms',
        help="""Get aggregated pool activity histogram information from pools in a specific poolgroup.  Requires admin role.""")
    getQueueHistograms_parser.set_defaults(func=poolmanager_get_queue_histograms)
    getQueueHistograms_parser.add_argument('--group', required=True, help="""The poolgroup to be described.""", action='store').completer = pool_group_completer

    # getFilesHistograms subparser
    getFilesHistograms_parser = poolmanager_subparser.add_parser(
        'getFilesHistograms',
        help="""Get aggregated file statistics histogram information from pools in a specific poolgroup.  Requires admin role.""")
    getFilesHistograms_parser.set_defaults(func=poolmanager_get_files_histograms)
    getFilesHistograms_parser.add_argument('--group', required=True, help="""The poolgroup to be described.""", action='store').completer = pool_group_completer

    # getLinks subparser
    getLinks_parser = poolmanager_subparser.add_parser(
        'getLinks',
        help="""Get information about all links.  Requires admin role. Results sorted lexicographically by link name.""")
    getLinks_parser.set_defaults(func=poolmanager_get_links)

    # getLinkGroups subparser
    getLinkGroups_parser = poolmanager_subparser.add_parser(
        'getLinkGroups',
        help="""Get information about all linkgroups.  Requires admin role. Results sorted lexicographically by link group name.""")
    getLinkGroups_parser.set_defaults(func=poolmanager_get_link_groups)

    # getPartitions subparser
    getPartitions_parser = poolmanager_subparser.add_parser(
        'getPartitions',
        help="""Get information about all partitions.  Requires admin role. Results sorted lexicographically by partition name.""")
    getPartitions_parser.set_defaults(func=poolmanager_get_partitions)

    # match subparser
    match_parser = poolmanager_subparser.add_parser(
        'match',
        help="""Describe the pools selected by a particular request.""")
    match_parser.set_defaults(func=poolmanager_match)
    match_parser.add_argument('--type', required=False, help="""The operation type.""", default='READ', action='store', choices=['READ', 'CACHE', 'WRITE', 'P2P', 'ANY'])
    match_parser.add_argument('--store', required=False, help="""The name of the matching store unit.""", default='*', action='store')
    match_parser.add_argument('--dcache', required=False, help="""The name of the matching dcache unit.""", default='*', action='store')
    match_parser.add_argument('--net', required=False, help="""The name of the matching net unit.""", default='*', action='store')
    match_parser.add_argument('--protocol', required=False, help="""The matching protocol unit.""", default='*', action='store')
    match_parser.add_argument('--linkGroup', required=False, help="""The linkgroup unit, or 'none' for a request outside of a linkgroup.""", default='none', action='store')

    # getUnits subparser
    getUnits_parser = poolmanager_subparser.add_parser(
        'getUnits',
        help="""List all units.  Requires admin role. Results sorted lexicographically by unit name.""")
    getUnits_parser.set_defaults(func=poolmanager_get_units)

    # getUnitGroups subparser
    getUnitGroups_parser = poolmanager_subparser.add_parser(
        'getUnitGroups',
        help="""List all unitgroups.  Requires admin role. Results sorted lexicographically by unit group name.""")
    getUnitGroups_parser.set_defaults(func=poolmanager_get_unit_groups)
    # The pools subparser
    pools_parser = subparsers.add_parser(
        'pools',
        help='File data storage',
        add_help=True)
    pools_parser.set_defaults(func=pools_parser.print_help)
    pools_subparser = pools_parser.add_subparsers()

    # getPool subparser
    getPool_parser = pools_subparser.add_parser(
        'getPool',
        help="""Get information about a specific pool (name, group membership, links). Requires admin role.""")
    getPool_parser.set_defaults(func=pools_get_pool)
    getPool_parser.add_argument('--pool', required=True, help="""The pool to be described.""", action='store').completer = pool_completer

    # getMovers subparser
    getMovers_parser = pools_subparser.add_parser(
        'getMovers',
        help="""Get mover information for a specific pool.  Requires admin role.""")
    getMovers_parser.set_defaults(func=pools_get_movers)
    getMovers_parser.add_argument('--pool', required=True, help="""The pool to be described.""", action='store').completer = pool_completer
    getMovers_parser.add_argument('--type', required=False, help="""A comma-seperated list of mover types. Currently, either 'p2p-client,p2p-server' or none (meaning all) is supported.""", action='store')
    getMovers_parser.add_argument('--offset', required=False, help="""The number of items to skip.""", type=int)
    getMovers_parser.add_argument('--limit', required=False, help="""The maximum number of items to return.""", type=int)
    getMovers_parser.add_argument('--pnfsid', required=False, help="""Select movers operating on a specific PNFS-ID.""", action='store')
    getMovers_parser.add_argument('--queue', required=False, help="""Select movers with a specific queue.""", action='store')
    getMovers_parser.add_argument('--state', required=False, help="""Select movers in a particular state.""", action='store')
    getMovers_parser.add_argument('--mode', required=False, help="""Select movers with a specific mode.""", action='store')
    getMovers_parser.add_argument('--door', required=False, help="""Select movers initiated by a specific door.""", action='store')
    getMovers_parser.add_argument('--storageClass', required=False, help="""Select movers with a specific storage class.""", action='store')
    getMovers_parser.add_argument('--sort', required=False, help="""How returned items should be sorted.""", default='door,startTime', action='store')

    # getQueueHistograms subparser
    getQueueHistograms_parser = pools_subparser.add_parser(
        'getQueueHistograms',
        help="""Get histogram data concerning activity on a specific pool (48-hour window).""")
    getQueueHistograms_parser.set_defaults(func=pools_get_queue_histograms)
    getQueueHistograms_parser.add_argument('--pool', required=True, help="""The pool to be described.""", action='store').completer = pool_completer

    # getFilesHistograms subparser
    getFilesHistograms_parser = pools_subparser.add_parser(
        'getFilesHistograms',
        help="""Get histogram data concerning file lifetime on a specific pool (60-day window).""")
    getFilesHistograms_parser.set_defaults(func=pools_get_files_histograms)
    getFilesHistograms_parser.add_argument('--pool', required=True, help="""The pool to be described.""", action='store').completer = pool_completer

    # getPoolUsage subparser
    getPoolUsage_parser = pools_subparser.add_parser(
        'getPoolUsage',
        help="""Get information about a specific pool (configuration, state, usage).  Requires admin role.""")
    getPoolUsage_parser.set_defaults(func=pools_get_pool_usage)
    getPoolUsage_parser.add_argument('--pool', required=True, help="""The pool to be described.""", action='store').completer = pool_completer

    # getRepositoryInfoForFile subparser
    getRepositoryInfoForFile_parser = pools_subparser.add_parser(
        'getRepositoryInfoForFile',
        help="""Get information about a specific PNFS-ID usage within a specific pool.  Requires admin role.""")
    getRepositoryInfoForFile_parser.set_defaults(func=pools_get_repository_info_for_file)
    getRepositoryInfoForFile_parser.add_argument('--pool', required=True, help="""The pool to be described.""", action='store').completer = pool_completer
    getRepositoryInfoForFile_parser.add_argument('--pnfsid', required=True, help="""The PNFS-ID of the file to be described.""", action='store')

    # getNearlineQueues subparser
    getNearlineQueues_parser = pools_subparser.add_parser(
        'getNearlineQueues',
        help="""Get nearline activity information for a specific pool.  Requires admin role.""")
    getNearlineQueues_parser.set_defaults(func=pools_get_nearline_queues)
    getNearlineQueues_parser.add_argument('--pool', required=True, help="""The pool to be described.""", action='store').completer = pool_completer
    getNearlineQueues_parser.add_argument('--type', required=False, help="""Select transfers of a specific type (flush, stage, remove).""", action='store')
    getNearlineQueues_parser.add_argument('--offset', required=False, help="""The number of items to skip.""", type=int)
    getNearlineQueues_parser.add_argument('--limit', required=False, help="""The maximum number of items to return.""", type=int)
    getNearlineQueues_parser.add_argument('--pnfsid', required=False, help="""Select only operations affecting this PNFS-ID.""", action='store')
    getNearlineQueues_parser.add_argument('--state', required=False, help="""Select only operations in this state.""", action='store')
    getNearlineQueues_parser.add_argument('--storageClass', required=False, help="""Select only operations of this storage class.""", action='store')
    getNearlineQueues_parser.add_argument('--sort', required=False, help="""How the returned values should be sorted.""", default='class,created', action='store')

    # killMovers subparser
    killMovers_parser = pools_subparser.add_parser(
        'killMovers',
        help="""Kill a mover.  Requires admin role.""")
    killMovers_parser.set_defaults(func=pools_kill_movers)
    killMovers_parser.add_argument('--pool', required=True, help="""The pool with the mover to be killed.""", action='store').completer = pool_completer
    killMovers_parser.add_argument('--id', required=True, help="""The id of the mover to be killed.""", type=int)

    # updateMode subparser
    updateMode_parser = pools_subparser.add_parser(
        'updateMode',
        help="""Modify a pool's mode.  Requires admin role.""")
    updateMode_parser.set_defaults(func=pools_update_mode)
    updateMode_parser.add_argument('--pool', required=True, help="""The pool affected by the mode change.""", action='store').completer = pool_completer
    updateMode_parser.add_argument('--body', required=True, help="""JSON object describing how the pool should be modified. (Corresponds to PoolModeUpdate.)""", action='store')

    # getPools subparser
    getPools_parser = pools_subparser.add_parser(
        'getPools',
        help="""Get information about all pools (name, group membership, links).  Requires admin role.  Results sorted lexicographically by pool name.""")
    getPools_parser.set_defaults(func=pools_get_pools)

    # getRestores subparser
    getRestores_parser = pools_subparser.add_parser(
        'getRestores',
        help="""Obtain a (potentially partial) list of restore operations from some snapshot, along with a token that identifies the snapshot.""")
    getRestores_parser.set_defaults(func=pools_get_restores)
    getRestores_parser.add_argument('--token', required=False, help="""Use the snapshot corresponding to this UUID.  The contract with the service is that if the parameter value is null, the current snapshot will be used, regardless of whether offset and limit are still valid.  Initial/refresh calls should always be without a token.  Subsequent calls should send back the current token; in the case that it no longer corresponds to the current list, the service will return a null token and an empty list, and the client will need to recall the method without a token (refresh).""", action='store')
    getRestores_parser.add_argument('--offset', required=False, help="""The number of restores to skip.""", type=int)
    getRestores_parser.add_argument('--limit', required=False, help="""The maximum number of restores to return.""", type=int)
    getRestores_parser.add_argument('--pnfsid', required=False, help="""Select only restores that affect this PNFS-ID.""", action='store')
    getRestores_parser.add_argument('--subnet', required=False, help="""Select only restores triggered by clients from this subnet.""", action='store')
    getRestores_parser.add_argument('--pool', required=False, help="""Select only restores on this pool.""", action='store').completer = pool_completer
    getRestores_parser.add_argument('--status', required=False, help="""Select only restores with this status.""", action='store')
    getRestores_parser.add_argument('--sort', required=False, help="""A comma-seperated list of fields on which to sort the results.""", default='pool,started', action='store')
    # The qos subparser
    qos_parser = subparsers.add_parser(
        'qos',
        help='Managing how data is stored and handled',
        add_help=True)
    qos_parser.set_defaults(func=qos_parser.print_help)
    qos_subparser = qos_parser.add_subparsers()

    # getQosList subparser
    getQosList_parser = qos_subparser.add_parser(
        'getQosList',
        help="""List the available quality of services for a specific object type.  Requires authentication.""")
    getQosList_parser.set_defaults(func=qos_get_qos_list)
    getQosList_parser.add_argument('--type', required=True, help="""The kind of object to query.""", action='store', choices=['file', 'directory'])

    # getQueriedQosForFiles subparser
    getQueriedQosForFiles_parser = qos_subparser.add_parser(
        'getQueriedQosForFiles',
        help="""Provide information about a specific file quality of services.  Requires authentication.""")
    getQueriedQosForFiles_parser.set_defaults(func=qos_get_queried_qos_for_files)
    getQueriedQosForFiles_parser.add_argument('--qos', required=True, help="""The file quality of service to query.""", action='store')

    # getQueriedQosForDirectories subparser
    getQueriedQosForDirectories_parser = qos_subparser.add_parser(
        'getQueriedQosForDirectories',
        help="""Provides information about a specific directory quality of services.  Requires authentication.""")
    getQueriedQosForDirectories_parser.set_defaults(func=qos_get_queried_qos_for_directories)
    getQueriedQosForDirectories_parser.add_argument('--qos', required=True, help="""The directory quality of service to query.""", action='store')
    # The spacemanager subparser
    spacemanager_parser = subparsers.add_parser(
        'spacemanager',
        help='Ensuring enough capacity for uploads',
        add_help=True)
    spacemanager_parser.set_defaults(func=spacemanager_parser.print_help)
    spacemanager_subparser = spacemanager_parser.add_subparsers()

    # getTokensForGroup subparser
    getTokensForGroup_parser = spacemanager_subparser.add_parser(
        'getTokensForGroup',
        help="""Get information about space tokens.  Requires admin role.  Results sorted by token id.""")
    getTokensForGroup_parser.set_defaults(func=spacemanager_get_tokens_for_group)
    getTokensForGroup_parser.add_argument('--id', required=False, help="""The id of the space token.""", type=int)
    getTokensForGroup_parser.add_argument('--voGroup', required=False, help="""VO group associated with the token.""", action='store')
    getTokensForGroup_parser.add_argument('--voRole', required=False, help="""VO role associated with the token.""", action='store')
    getTokensForGroup_parser.add_argument('--accessLatency', required=False, help="""Access Latency associated with the token.""", action='store')
    getTokensForGroup_parser.add_argument('--retentionPolicy', required=False, help="""Retention Policy associated with the token.""", action='store')
    getTokensForGroup_parser.add_argument('--groupId', required=False, help="""Id of link group to which token belongs.""", type=int)
    getTokensForGroup_parser.add_argument('--state', required=False, help="""State of the token.""", action='store')
    getTokensForGroup_parser.add_argument('--minSize', required=False, help="""Minimum size (in bytes) of token.""", type=int)
    getTokensForGroup_parser.add_argument('--minFreeSpace', required=False, help="""Minimum amount of space (in bytes) still free for token.""", type=int)

    # getLinkGroups subparser
    getLinkGroups_parser = spacemanager_subparser.add_parser(
        'getLinkGroups',
        help="""Get information about link groups.  Requires admin role. Results sorted lexicographically by link group name.""")
    getLinkGroups_parser.set_defaults(func=spacemanager_get_link_groups)
    getLinkGroups_parser.add_argument('--name', required=False, help="""The name of the link group.""", action='store')
    getLinkGroups_parser.add_argument('--id', required=False, help="""The id of the link group.""", type=int)
    getLinkGroups_parser.add_argument('--onlineAllowed', required=False, help="""Whether the link group allows online access latency.""", action='store_true')
    getLinkGroups_parser.add_argument('--nearlineAllowed', required=False, help="""Whether the link group allows nearline access latency.""", action='store_true')
    getLinkGroups_parser.add_argument('--replicaAllowed', required=False, help="""Whether the link group allows replica retention policy.""", action='store_true')
    getLinkGroups_parser.add_argument('--outputAllowed', required=False, help="""Whether the link group allows output retention policy.""", action='store_true')
    getLinkGroups_parser.add_argument('--custodialAllowed', required=False, help="""Whether the link group allows custodial retention policy.""", action='store_true')
    getLinkGroups_parser.add_argument('--voGroup', required=False, help="""VO group associated with the link.""", action='store')
    getLinkGroups_parser.add_argument('--voRole', required=False, help="""VO role associated with the link.""", action='store')
    getLinkGroups_parser.add_argument('--minAvailableSpace', required=False, help="""Minimum amount of space (in bytes) still available via the link.""", type=int)
    # The transfers subparser
    transfers_parser = subparsers.add_parser(
        'transfers',
        help='The movement of data between dCache and clients',
        add_help=True)
    transfers_parser.set_defaults(func=transfers_parser.print_help)
    transfers_subparser = transfers_parser.add_subparsers()

    # getTransfers subparser
    getTransfers_parser = transfers_subparser.add_parser(
        'getTransfers',
        help="""Provide a list of all client-initiated transfers that are either queued or currently running.  Internal (pool-to-pool) transfers are excluded.""")
    getTransfers_parser.set_defaults(func=transfers_get_transfers)
    getTransfers_parser.add_argument('--token', required=False, help="""Use the snapshot corresponding to this UUID.  The contract with the service is that if the parameter value is null, the current snapshot will be used, regardless of whether offset and limit are still valid.  Initial/refresh calls should always be without a token.  Subsequent calls should send back the current token; in the case that it no longer corresponds to the current list, the service will return a null token and an empty list, and the client will need to recall the method without a token (refresh).""", action='store')
    getTransfers_parser.add_argument('--offset', required=False, help="""The number of items to skip.""", type=int)
    getTransfers_parser.add_argument('--limit', required=False, help="""The maximum number items to return.""", type=int)
    getTransfers_parser.add_argument('--state', required=False, help="""Select transfers in this state (NOTFOUND, STAGING, QUEUED, RUNNING, CANCELED, DONE)""", action='store')
    getTransfers_parser.add_argument('--door', required=False, help="""Select transfers initiated through this door.""", action='store')
    getTransfers_parser.add_argument('--domain', required=False, help="""Select transfers initiated through a door in this domain.""", action='store')
    getTransfers_parser.add_argument('--prot', required=False, help="""Select transfers using this protocol.""", action='store')
    getTransfers_parser.add_argument('--uid', required=False, help="""Select transfers initiated by this user.""", action='store')
    getTransfers_parser.add_argument('--gid', required=False, help="""Select transfers initiated by a member of this group.""", action='store')
    getTransfers_parser.add_argument('--vomsgroup', required=False, help="""Select transfers initiated by a member of this vomsgroup.""", action='store')
    getTransfers_parser.add_argument('--pnfsid', required=False, help="""Select transfers involving this pnfsid.""", action='store')
    getTransfers_parser.add_argument('--pool', required=False, help="""Select transfers involving this pool.""", action='store').completer = pool_completer
    getTransfers_parser.add_argument('--client', required=False, help="""Select transfers involving this client.""", action='store')
    getTransfers_parser.add_argument('--sort', required=False, help="""A comma-seperated list of fields to sort the responses.""", default='door,waiting', action='store')
    # The events subparser
    events_parser = subparsers.add_parser(
        'events',
        help='Support for SSE clients receiving dCache events',
        add_help=True)
    events_parser.set_defaults(func=events_parser.print_help)
    events_subparser = events_parser.add_subparsers()

    # channelMetadata subparser
    channelMetadata_parser = events_subparser.add_parser(
        'channelMetadata',
        help="""Obtain metadata about a channel.""")
    channelMetadata_parser.set_defaults(func=events_channel_metadata)
    channelMetadata_parser.add_argument('--id', required=True, help="""None""", action='store')

    # deleteChannel subparser
    deleteChannel_parser = events_subparser.add_parser(
        'deleteChannel',
        help="""Cancel a channel.""")
    deleteChannel_parser.set_defaults(func=events_delete_channel)
    deleteChannel_parser.add_argument('--id', required=True, help="""None""", action='store')

    # modify subparser
    modify_parser = events_subparser.add_parser(
        'modify',
        help="""Modify a channel.""")
    modify_parser.set_defaults(func=events_modify)
    modify_parser.add_argument('--id', required=True, help="""None""", action='store')
    modify_parser.add_argument('--body', required=False, help="""None""", action='store')

    # getChannels subparser
    getChannels_parser = events_subparser.add_parser(
        'getChannels',
        help="""Obtain a list of channels.""")
    getChannels_parser.set_defaults(func=events_get_channels)
    getChannels_parser.add_argument('--client-id', required=False, help="""Limit channels by client-id""", action='store')

    # register subparser
    register_parser = events_subparser.add_parser(
        'register',
        help="""Request a new channel.""")
    register_parser.set_defaults(func=events_register)
    register_parser.add_argument('--body', required=False, help="""None""", action='store')

    # channelSubscription subparser
    channelSubscription_parser = events_subparser.add_parser(
        'channelSubscription',
        help="""Return the selector of this subscription.""")
    channelSubscription_parser.set_defaults(func=events_channel_subscription)
    channelSubscription_parser.add_argument('--channel_id', required=True, help="""None""", action='store')
    channelSubscription_parser.add_argument('--type', required=True, help="""None""", action='store')
    channelSubscription_parser.add_argument('--subscription_id', required=True, help="""None""", action='store')

    # delete subparser
    delete_parser = events_subparser.add_parser(
        'delete',
        help="""Cancel a subscription.""")
    delete_parser.set_defaults(func=events_delete)
    delete_parser.add_argument('--channel_id', required=True, help="""None""", action='store')
    delete_parser.add_argument('--type', required=True, help="""None""", action='store')
    delete_parser.add_argument('--subscription_id', required=True, help="""None""", action='store')

    # subscribe subparser
    subscribe_parser = events_subparser.add_parser(
        'subscribe',
        help="""Subscribe to events.""")
    subscribe_parser.set_defaults(func=events_subscribe)
    subscribe_parser.add_argument('--id', required=True, help="""None""", action='store')
    subscribe_parser.add_argument('--type', required=True, help="""None""", action='store')
    subscribe_parser.add_argument('--body', required=False, help="""None""", action='store')

    # channelSubscriptions subparser
    channelSubscriptions_parser = events_subparser.add_parser(
        'channelSubscriptions',
        help="""Obtain list a channel's subscriptions.""")
    channelSubscriptions_parser.set_defaults(func=events_channel_subscriptions)
    channelSubscriptions_parser.add_argument('--id', required=True, help="""None""", action='store')

    # getEventTypes subparser
    getEventTypes_parser = events_subparser.add_parser(
        'getEventTypes',
        help="""Obtain a list of the available event types.""")
    getEventTypes_parser.set_defaults(func=events_get_event_types)

    # getSelectorSchema subparser
    getSelectorSchema_parser = events_subparser.add_parser(
        'getSelectorSchema',
        help="""Obtain the JSON schema for this event type's selectors.""")
    getSelectorSchema_parser.set_defaults(func=events_get_selector_schema)
    getSelectorSchema_parser.add_argument('--type', required=True, help="""The specific event type to be described.""", action='store')

    # getEventSchema subparser
    getEventSchema_parser = events_subparser.add_parser(
        'getEventSchema',
        help="""Obtain the JSON schema for events of this event type.""")
    getEventSchema_parser.set_defaults(func=events_get_event_schema)
    getEventSchema_parser.add_argument('--type', required=True, help="""The specific event type to be described.""", action='store')

    # serviceMetadata subparser
    serviceMetadata_parser = events_subparser.add_parser(
        'serviceMetadata',
        help="""Obtain general information about event support in dCache.""")
    serviceMetadata_parser.set_defaults(func=events_service_metadata)

    # getEventType subparser
    getEventType_parser = events_subparser.add_parser(
        'getEventType',
        help="""Obtain non-schema information about a specific event type.""")
    getEventType_parser.set_defaults(func=events_get_event_type)
    getEventType_parser.add_argument('--type', required=True, help="""The specific event type to be described.""", action='store')

    # bring-online
    bringonline_parser = namespace_subparser.add_parser(
        'bring-online',
        help='Stage file or bring a file online.')
    bringonline_parser.add_argument('--path', required=True, help="""Path of file to stage.""", action='store').completer = path_completer
    bringonline_parser.set_defaults(func=bring_online)

    # The sync subparser
    sync_parser = subparsers.add_parser(
        'sync',
        help='Synchronise storage')
    sync_parser.set_defaults(func=sync_storage)
    sync_parser.add_argument(
        '--root_path', default=None, required=True,
        help="The root path.")
    sync_parser.add_argument(
        '--destination', dest="destination", required=True,
        help="The destination url.")
    sync_parser.add_argument(
        '--source', dest="source", required=True,
        help="The source url.")
    sync_parser.add_argument(
        '--fts_host', dest="fts_host", required=True,
        help="The FTS host name.")
    sync_parser.add_argument(
        '--recursive', '-r',
        action='store_const',
        const=True,
        default=False,
        help='Recursively sync subdirectories.')
    return oparser


def main():
    '''Main method.'''
    config = get_config()
    oparser = get_parser(config)
    argcomplete.autocomplete(oparser)
    args = oparser.parse_args(sys.argv[1:])
    if args.debug:
        ROOTLOGGER.setLevel(logging.DEBUG)
    else:
        ROOTLOGGER.setLevel(logging.INFO)

    disable_warnings()
    if args.func.__name__ == 'print_help':
        args.func()
    else:
        args.func(args)

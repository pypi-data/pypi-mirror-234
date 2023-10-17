"""Import FedRAMP Revision 4 SSP XML into RegScale"""
# flake8: noqa
from typing import Dict, Tuple

from lxml import etree
from lxml.etree import Element
from pydantic import ValidationError

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.internal.file_uploads import file_upload
from regscale.core.app.logz import create_logger
from regscale.core.app.public.fedramp.fedramp_traversal import FedrampTraversal
from regscale.core.app.public.fedramp.metadata import parse_metadata
from regscale.core.app.public.fedramp.reporting import write_events
from regscale.core.app.public.fedramp.system_characteristics import (
    parse_minimum_ssp,
    parse_system_characteristics,
)
from regscale.core.app.public.fedramp.system_control_implementations import (
    fetch_implementations,
)
from regscale.core.app.public.fedramp.system_implementation import (
    parse_system_implementation,
)
from regscale.core.app.utils.app_utils import get_file_name
from regscale.core.app.utils.regscale_utils import create_new_data_submodule
from regscale.models.regscale_models.files import File
from regscale.models.regscale_models.properties import Properties
from regscale.models.regscale_models.securityplans import SecurityPlan

logger = create_logger()


def parse_and_load_xml_rev4(
    file_path,
    catalouge_id: int,
    filename: str = "Sample.xml",
) -> Tuple[str, Dict, Dict]:
    """
     Parse and load XML Rev4
    :param str file_path: Path to XML file
    :param int catalouge_id: Catalogue ID user selected
    :param str filename: Name of file that will be uploaded to RegScale
    :return: Tuple of filename and upload results
    :rtype: Tuple[str, Dict]
    """
    logger.info(f"Parsing and loading XML Rev4 file {file_path}.")
    events_list = (
        []
    )  # will store events as they take place throughout the import process
    app = Application()
    api = Api(app)
    events_list = (
        []
    )  # will store events as they take place throughout the import process

    ns = {
        "ns1": "http://csrc.nist.gov/ns/oscal/1.0",
        "oscal": "http://csrc.nist.gov/ns/oscal/1.0",
        "fedramp": "https://fedramp.gov/ns/oscal",
    }

    tree = etree.parse(file_path)
    root = tree.getroot()
    ssp_uuid = root.attrib["uuid"]
    new_ssp = {"uuid": ssp_uuid}

    # Create fedramp traversal object.
    trv = FedrampTraversal(
        api=api,
        root=root,
        namespaces=ns,
    )
    # --- Set the catalogue_id on the traversal object.
    trv.catalogue_id = catalouge_id

    # 0. Create the EMPTY SSP that we need for later posts.
    ssp_id = parse_minimum_ssp(
        api=api, root=root, new_ssp=new_ssp, ns=ns, events_list=events_list
    )
    logger.info(f"Created new SSP in RegScale with ID {ssp_id}.")
    # --- Set the ssp_id on the traversal object.
    trv.ssp_id = ssp_id

    # 1. Parse the <metadata> tag
    parse_metadata(trv)

    # upload xml file & data submodules in the SSP
    attach_xml_to_ssp(trv=trv, file_path=file_path)

    # 2. Parse the <system-characteristics> tag
    parse_system_characteristics(
        ssp_id=ssp_id, root=root, ns=ns, events_list=events_list
    )
    logger.info("System characteristics parsed successfully.")

    # 3. Parse the <system-implementation> tag!
    parse_system_implementation(trv)

    # 4. TODO <control-implementation>
    # parse_control_implementation()

    # 5. Parse <back-matter>
    # parse_back_matter()

    # Write the events.
    final_list = [*events_list, *trv.errors, *trv.infos]
    write_events(final_list)

    # TODO: review with Josh
    # If data is incomplete This fails w/ 500 error ( which means the json string being received by the server is either malformed or missing something
    logger.info("Uploading SSP to RegScale...")
    try:
        ssp = SecurityPlan.from_dict(new_ssp)
    except ValidationError as exc:
        logger.error(f"Failed to validate: {exc}")
        return "artifacts/import-results.csv", {
            "status": "failed",
        }
    # you can create a new ssp without the userId populated, but we normally use the userId from init.yaml
    ssp.systemOwnerId = app.config["userId"]
    ssp.id = ssp_id
    new_ssp = ssp.update_ssp(api=api, return_id=False)
    new_ssp_id = new_ssp.id
    oscal_implementations = fetch_implementations(trv=trv, root=root, ssp=new_ssp)
    if oscal_implementations:
        implementation_results = {
            "status": "success",
            "ssp_id": new_ssp_id,
            "implementations_loaded": len(oscal_implementations),
        }

    # upload_results["implementations"] = implementation_results
    """ properties handling is getting moved. Comment out for now.
    properties_response = Properties.create_properties_from_list(
        parent_id=new_ssp_id,
        parent_module="securityplans",
        properties_list=properties_list,
    )
    upload_results["properties_response"] = properties_response
    """
    upload_results = {
        "ssp_id": new_ssp_id,
        "ssp_title": new_ssp.systemName,
    }
    logger.info(f"Finished uploading SSP {ssp_id}")
    # FIXME change this to the actual import.csv that is returned
    # upload privacyImpactAssessment. If is None then dont.

    return "artifacts/import-results.csv", upload_results, oscal_implementations


def attach_xml_to_ssp(trv: FedrampTraversal, file_path: str) -> None:
    """
    Function to attach the XML file to the SSP's data and file submodules in RegScale
    :param FedrampTraversal trv: FedrampTraversal object
    :param str file_path: Path to the file to upload
    :return: None
    """
    # upload xml file to SSP
    if File.upload_file_to_regscale(
        file_name=file_path,
        parent_id=trv.ssp_id,
        parent_module="securityplans",
        api=trv.api,
        return_object=True,
    ):
        trv.log_info(
            {
                "record_type": "file",
                "event_msg": f"Uploaded file '{get_file_name(file_path)}' to SSP# {get_file_name(file_path)}"
                "File module in RegScale.",
            }
        )
    else:
        trv.log_error(
            {
                "record_type": "file",
                "event_msg": f"Failed to upload file '{get_file_name(file_path)}' to SSP# {trv.ssp_id} "
                "File module in RegScale.",
            }
        )
    if create_new_data_submodule(
        api=trv.api,
        parent_id=trv.ssp_id,
        parent_module="securityplans",
        file_path=file_path,
    ):
        trv.log_info(
            {
                "record_type": "Data",
                "event_msg": f"Uploaded file '{get_file_name(file_path)}' to SSP# {get_file_name(file_path)}"
                "Data module in RegScale.",
            }
        )
    else:
        trv.log_error(
            {
                "record_type": "Data",
                "event_msg": f"Failed to upload file '{get_file_name(file_path)}' to SSP# {trv.ssp_id} "
                " Data module in RegScale.",
            }
        )

"""Library defining the interface to firewall."""
from datetime import timedelta
from typing import Any, Dict, Iterator, List, Optional

import pandas as pd
from deprecated import deprecated

from rime_sdk.internal.config_parser import (
    convert_single_data_info_to_swagger,
    convert_single_pred_info_to_swagger,
)
from rime_sdk.internal.constants import (
    MONITOR_TYPE_TO_SWAGGER,
    RISK_CATEGORY_TO_SWAGGER,
)
from rime_sdk.internal.decorators import prompt_confirmation
from rime_sdk.internal.rest_error_handler import RESTErrorHandler
from rime_sdk.internal.swagger_parser import parse_events_to_df
from rime_sdk.internal.swagger_utils import rest_to_timedelta
from rime_sdk.internal.throttle_queue import ThrottleQueue
from rime_sdk.internal.utils import convert_dict_to_html, make_link
from rime_sdk.job import ContinuousTestJob
from rime_sdk.monitor import Monitor
from rime_sdk.swagger import swagger_client
from rime_sdk.swagger.swagger_client import (
    ApiClient,
    ContinuoustestsFirewallIdUuidBody,
    FirewallFirewall,
    FirewallFirewallFirewallIdUuidBody,
    FirewallScheduledCTInfo,
    RimeUpdateFirewallResponse,
    RimeUUID,
    RuntimeinfoCustomImage,
    RuntimeinfoCustomImageType,
    RuntimeinfoResourceRequest,
    RuntimeinfoRunTimeInfo,
    TestrunTestRunIncrementalConfig,
    V1firewallfirewallFirewallIdUuidFirewall,
)
from rime_sdk.swagger.swagger_client.api.detection_api import DetectionApi
from rime_sdk.swagger.swagger_client.models import RimeJobMetadata
from rime_sdk.swagger.swagger_client.models.detection_event_type import (
    DetectionEventType,
)


@deprecated("Firewall class will not be supported from Robust Intelligence v2.4.")
class Firewall:
    """An interface to a RIME Firewall.

    **Note that the Firewall class is deprecated in Robust Intelligence v2.2
    and will be removed in v2.4. It will be replaced by the new ContinuousTest
    class.**
    """

    # A throttler that limits the number of model tests to roughly 20 every 5 minutes.
    # This is a static variable for Client.
    _throttler = ThrottleQueue(desired_events_per_epoch=20, epoch_duration_sec=300)

    def __init__(self, api_client: ApiClient, firewall_id: str) -> None:
        """Create a new Firewall object.

        Arguments:
            api_client: ApiClient
                The client used to query the RIME cluster.
            firewall_id: str
                The ID of the Firewall.
        """
        self._api_client = api_client
        self._firewall_id = firewall_id

    def __eq__(self, obj: Any) -> bool:
        """Check if this FWInstance is equivalent to 'obj'."""
        return isinstance(obj, Firewall) and self._firewall_id == obj._firewall_id

    def __repr__(self) -> str:
        """Return string representation of the object."""
        return f"Firewall({self._firewall_id})"

    @deprecated(
        "Firewall class methods will not be supported from Robust Intelligence v2.4."
    )
    def update_firewall(
        self,
        model_id: Optional[str] = None,
        ref_data_id: Optional[str] = None,
        scheduled_ct_eval_data_integration_id: Optional[str] = None,
        scheduled_ct_eval_data_info: Optional[dict] = None,
        scheduled_ct_eval_pred_integration_id: Optional[str] = None,
        scheduled_ct_eval_pred_info: Optional[dict] = None,
        disable_scheduled_ct: Optional[bool] = False,
    ) -> RimeUpdateFirewallResponse:
        """Update the Firewall with specified model and reference data.

        **Note that the Firewall is deprecated in Robust Intelligence v2.2 and
        will not be supported from v2.4. This method will be replaced by
        `update_ct` in the new ContinuousTest class.**

        Arguments:
            model_id: Optional[str]
                The ID of the model to use for the Firewall.
            ref_data_id: Optional[str]
                The ID of the reference data to use for the Firewall.
            scheduled_ct_eval_data_integration_id: Optional[str]
                The integration id of the evaluation data for scheduled CT.
            scheduled_ct_eval_data_info: Optional[Dict]
                The data info of the evaluation data for scheduled CT.
            scheduled_ct_eval_pred_integration_id: Optional[str]
                The integration id of the evaluation prediction for scheduled CT.
            scheduled_ct_eval_pred_info: Optional[Dict]
                The data info of the evaluation prediction for scheduled CT.
            disable_scheduled_ct: Optional[bool]
                Specifies whether to disable continuous testing

        Returns:
            Dict:
                Dictionary representation of updated Firewall object.

        Raises:
            ValueError
                This error is generated when no fields are submitted to be updated or
                when the request to the Firewall service fails.

        Example:
            .. code-block:: python

                response = fw.update_firewall(ref_data_id="New reference data ID")
        """
        api = swagger_client.FirewallServiceApi(self._api_client)
        field_mask_list = []
        if model_id is not None:
            field_mask_list.append("modelId")
        if ref_data_id is not None:
            field_mask_list.append("refDataId")
        scheduled_ct_info = FirewallScheduledCTInfo()
        if scheduled_ct_eval_data_integration_id is not None:
            field_mask_list.append("scheduledCtInfo.evalDataIntegrationId")
            scheduled_ct_info.eval_data_integration_id = RimeUUID(
                uuid=scheduled_ct_eval_data_integration_id
            )
        if scheduled_ct_eval_data_info is not None:
            field_mask_list.append("scheduledCtInfo.evalDataInfo")
            scheduled_ct_info.eval_data_info = convert_single_data_info_to_swagger(
                scheduled_ct_eval_data_info
            )
        if scheduled_ct_eval_pred_integration_id is not None:
            field_mask_list.append("scheduledCtInfo.evalPredIntegrationId")
            scheduled_ct_info.eval_pred_integration_id = RimeUUID(
                uuid=scheduled_ct_eval_pred_integration_id
            )
        if scheduled_ct_eval_pred_info is not None:
            field_mask_list.append("scheduledCtInfo.evalPredInfo")
            scheduled_ct_info.eval_pred_info = convert_single_pred_info_to_swagger(
                scheduled_ct_eval_pred_info
            )
        if disable_scheduled_ct:
            field_mask_list.append("scheduledCtInfo.disableScheduledCt")
            scheduled_ct_info.disable_scheduled_ct = disable_scheduled_ct
        if len(field_mask_list) == 0:
            raise ValueError(
                "User must provide at least one of model_id, ref_data_id, "
                "or scheduled CT paramaters."
            )
        req = FirewallFirewallFirewallIdUuidBody(
            firewall_id=RimeUUID(self._firewall_id),
            firewall=V1firewallfirewallFirewallIdUuidFirewall(
                model_id=RimeUUID(model_id) if model_id is not None else None,
                ref_data_id=ref_data_id,
                scheduled_ct_info=scheduled_ct_info,
            ),
            mask=",".join(field_mask_list),
        )
        with RESTErrorHandler():
            resp = api.firewall_service_update_firewall(
                firewall_firewall_id_uuid=self._firewall_id,
                body=req,
            )
        print(f"Firewall {self._firewall_id} updated successfully.")
        return resp

    @deprecated(
        "Firewall class methods will not be supported from Robust Intelligence v2.4."
    )
    def activate_ct_scheduling(
        self,
        data_info: dict,
        data_integration_id: Optional[str] = None,
        pred_integration_id: Optional[str] = None,
        pred_info: Optional[dict] = None,
    ) -> None:
        """Activate scheduled CT.

        **Note that the Firewall is deprecated in Robust Intelligence v2.2 and
        will not be supported from v2.4. This method will be replaced by
        `activate_ct_scheduling` in the new ContinuousTest class.**

        Arguments:
            data_info: dict
                The data info of the evaluation data for scheduled CT.
            data_integration_id: Optional[str]
                The integration id of the evaluation data for scheduled CT.
            pred_integration_id: Optional[str]
                The integration id of the evaluation prediction for scheduled CT.
            pred_info: Optional[dict]
                The prediction info of the evaluation data for scheduled CT.
        """
        if self.is_scheduled_ct_enabled():
            raise ValueError(
                "Scheduled CT is already enabled. Please use "
                "`update_scheduled_ct_info` to update the location info."
            )
        self.update_firewall(
            scheduled_ct_eval_data_integration_id=data_integration_id,
            scheduled_ct_eval_data_info=data_info,
            scheduled_ct_eval_pred_integration_id=pred_integration_id,
            scheduled_ct_eval_pred_info=pred_info,
            disable_scheduled_ct=False,
        )
        print(f"Scheduled CT of Firewall {self._firewall_id} activated successfully.")

    @deprecated(
        "Firewall class methods will not be supported from Robust Intelligence v2.4."
    )
    def update_scheduled_ct_info(
        self,
        data_integration_id: Optional[str] = None,
        data_info: Optional[dict] = None,
        pred_integration_id: Optional[str] = None,
        pred_info: Optional[dict] = None,
    ) -> None:
        """Update scheduled CT.

        **Note that the Firewall is deprecated in Robust Intelligence v2.2 and
        will not be supported from v2.4. This method will be replaced by
        `update_scheduled_ct_info` in the new ContinuousTest class.**

        Arguments:
            data_integration_id: Optional[str]
                If `data_integration_id` is not `None`, the Firewall will use it
                for scheduled CT.
            data_info: Optional[dict]
                If `data_info` is not `None`, the Firewall will use it for
                scheduled CT.
            pred_integration_id: Optional[str]
                If `pred_integration_id` is not `None`, the Firewall will use it
                for scheduled CT.
            pred_info: Optional[dict]
                If `pred_info` is not `None`, the Firewall will use it for scheduled CT.
        """
        self.update_firewall(
            scheduled_ct_eval_data_integration_id=data_integration_id,
            scheduled_ct_eval_data_info=data_info,
            scheduled_ct_eval_pred_integration_id=pred_integration_id,
            scheduled_ct_eval_pred_info=pred_info,
        )
        print(f"Location info of Firewall {self._firewall_id} updated successfully.")

    @deprecated(
        "Firewall class methods will not be supported from Robust Intelligence v2.4."
    )
    def deactivate_ct_scheduling(self) -> None:
        """Deactivate scheduled CT.

        **Note that the Firewall is deprecated in Robust Intelligence v2.2 and
        will not be supported from v2.4. This method will be replaced by
        `deactivate_ct_scheduling` in the new ContinuousTest class.**
        """
        if not self.is_scheduled_ct_enabled():
            raise ValueError("Scheduled CT is already disabled.")
        self.update_firewall(disable_scheduled_ct=True)
        print(f"Scheduled CT of Firewall {self._firewall_id} deactivated successfully.")

    def _repr_html_(self) -> str:
        """Return HTML representation of the object."""
        info = {
            "Firewall ID": self._firewall_id,
            "Link": make_link(
                "https://" + self.get_link(),
                link_text="Continuous Testing Overview Page",
            ),
        }
        return convert_dict_to_html(info)

    @deprecated(
        "Firewall class methods will not be supported from Robust Intelligence v2.4."
    )
    def get_link(self) -> str:
        """Return a URL to the Firewall.

        **Note that the Firewall is deprecated in Robust Intelligence v2.2 and
        will not be supported from v2.4. This method will be replaced by
        `get_link` in the new ContinuousTest class.**
        """
        api = swagger_client.FirewallServiceApi(self._api_client)
        with RESTErrorHandler():
            resp = api.firewall_service_get_url(
                firewall_id_uuid=self._firewall_id,
            )
        return resp.url.url

    @deprecated(
        "Firewall class methods will not be supported from Robust Intelligence v2.4."
    )
    def get_bin_size(self) -> timedelta:
        """Return the bin size of this Firewall.

        **Note that the Firewall is deprecated in Robust Intelligence v2.2 and
        will not be supported from v2.4. This method will be replaced by
        `get_bin_size` in the new ContinuousTest class.**
        """
        firewall = self._get_firewall()
        return rest_to_timedelta(firewall.bin_size)

    @deprecated(
        "Firewall class methods will not be supported from Robust Intelligence v2.4."
    )
    def get_ref_data_id(self) -> str:
        """Return the ID of the Firewall's current reference set.

        **Note that the Firewall is deprecated in Robust Intelligence v2.2 and
        will not be supported from v2.4. This method will be replaced by
        `get_ref_data_id` in the new ContinuousTest class.**
        """
        firewall = self._get_firewall()
        return firewall.ref_data_id

    @deprecated(
        "Firewall class methods will not be supported from Robust Intelligence v2.4."
    )
    def get_model_id(self) -> str:
        """Return the ID of the Firewall's current model.

        **Note that the Firewall is deprecated in Robust Intelligence v2.2 and
        will not be supported from v2.4. This method will be replaced by
        `get_model_id` in the new ContinuousTest class.**
        """
        firewall = self._get_firewall()
        return firewall.model_id.uuid

    @deprecated(
        "Firewall class methods will not be supported from Robust Intelligence v2.4."
    )
    def get_scheduled_ct_info(self) -> FirewallScheduledCTInfo:
        """Return the scheduled continuous testing info of this Firewall.

        **Note that the Firewall is deprecated in Robust Intelligence v2.2 and
        will not be supported from v2.4. This method will be replaced by
        `get_scheduled_ct_info` in the new ContinuousTest class.**
        """
        firewall = self._get_firewall()
        return firewall.scheduled_ct_info

    @deprecated(
        "Firewall class methods will not be supported from Robust Intelligence v2.4."
    )
    def is_scheduled_ct_enabled(self) -> bool:
        """Return whether scheduled continuous testing is enabled for this Firewall.

        **Note that the Firewall is deprecated in Robust Intelligence v2.2 and
        will not be supported from v2.4. This method will be replaced by
        `is_scheduled_ct_enabled` in the new ContinuousTest class.**
        """
        firewall = self._get_firewall()
        is_enabled = firewall.scheduled_ct_info is not None
        is_enabled = is_enabled and not firewall.scheduled_ct_info.disable_scheduled_ct
        return is_enabled

    @property
    def project_id(self) -> str:
        """Return the ID of the parent project for this Firewall.

        **Note that the Firewall is deprecated in Robust Intelligence v2.2 and
        will not be supported from v2.4. This method will be replaced by
        `project_id` in the new ContinuousTest class.**
        """
        fw = self._get_firewall()
        return fw.project_id.uuid

    @deprecated(
        "Firewall class methods will not be supported from Robust Intelligence v2.4."
    )
    @prompt_confirmation("Are you sure you want to delete this Firewall? (y/n) ")
    def delete_firewall(
        self,
        force: Optional[bool] = False,  # noqa: ARG002 (unused-method-argument)
    ) -> None:
        """Delete Firewall.

        **Note that the Firewall is deprecated in Robust Intelligence v2.2 and
        will not be supported from v2.4. This method will be replaced by
        `delete_ct` in the new ContinuousTest class.**

        Args:
            force: Optional[bool] = False
                When set to True, the Firewall will be deleted immediately. By default,
                a confirmation is required.
        """
        api = swagger_client.FirewallServiceApi(self._api_client)
        with RESTErrorHandler():
            api.firewall_service_delete_firewall(firewall_id_uuid=self._firewall_id)
        print("Firewall successfully deleted.")

    def _get_firewall(self) -> FirewallFirewall:
        api = swagger_client.FirewallServiceApi(self._api_client)
        with RESTErrorHandler():
            res = api.firewall_service_get_firewall(firewall_id_uuid=self._firewall_id)
        return res.firewall

    @deprecated(
        "Firewall class methods will not be supported from Robust Intelligence v2.4."
    )
    def get_events_df(
        self,
    ) -> pd.DataFrame:
        """Get a dataframe of Detected Events for the given Firewall.

        **Note that the Firewall is deprecated in Robust Intelligence v2.2 and
        will not be supported from v2.4. This method will be replaced by
        `get_events_df` in the new ContinuousTest class.**

        Monitors detect Events when degradations occur.
        For example, a Monitor for the metric "Accuracy" will detect an Event
        when the value of the model performance metric drops below a threshold.
        """
        detection_api = DetectionApi(self._api_client)
        next_page_token = ""
        has_more = True
        all_events = []
        while has_more:
            kwargs: Dict[str, Any] = {}
            if len(next_page_token) > 0:
                kwargs["page_token"] = next_page_token
            else:
                # Restrict to events for CT.
                kwargs["first_page_req_event_types"] = [
                    DetectionEventType.METRIC_DEGRADATION,
                    DetectionEventType.SECURITY,
                ]
            with RESTErrorHandler():
                res = detection_api.detection_list_detection_events(
                    self.project_id, **kwargs
                )
                next_page_token = res.next_page_token
                has_more = res.has_more
                all_events += res.events
        df = parse_events_to_df(all_events)
        return df

    @deprecated(
        "Firewall class methods will not be supported from Robust Intelligence v2.4."
    )
    def list_monitors(
        self,
        monitor_types: Optional[List[str]] = None,
        risk_category_types: Optional[List[str]] = None,
    ) -> Iterator[Monitor]:
        """List Monitors for the given Firewall.

        **Note that the Firewall is deprecated in Robust Intelligence v2.2 and
        will not be supported from v2.4. This method will be replaced by
        `list_monitors` in the new ContinuousTest class.**

        Monitors examine time-sequenced data in RIME. Built-in Monitors track model
        health metrics such as degradations in model performance metrics or attacks
        on your model. This method can optionally filter by Monitor types or Risk
        Category types.

        Arguments:
            monitor_types: Optional[List[str]]
                Modifies query to return the set of built-in monitors or
                user-created custom monitors.
                Accepted values: ["Default", "Custom"]
            risk_category_types: Optional[List[str]]
                Modifies query to return monitors pertaining to certain categories
                of AI Risk. For instance, monitors that track model performance help
                you track down Operational Risk.
                Accepted values: \
                ["Operational", "Bias_and_Fairness", "Security", "Custom"]

        Returns:
            Iterator[Monitor]:
                A generator of Monitor objects.

        Raises:
            ValueError
                This error is generated when unrecognized filtering parameters are
                provided or when the request to the Firewall service fails.

        Example:
            .. code-block:: python

                # List all default Monitors on the Firewall
                monitors = firewall.list_monitors(monitor_types=["Default"])
                # For each Monitor, list all detected Events.
                all_events = [monitor.list_detected_events() for monitor in monitors]
        """
        swagger_monitor_types = []
        swagger_risk_types = []
        if monitor_types is not None:
            try:
                swagger_monitor_types = [
                    MONITOR_TYPE_TO_SWAGGER[m] for m in monitor_types
                ]
            except KeyError as e:
                raise ValueError(
                    f"{e.args[0]} is not a valid monitor type,"
                    + f" {list(MONITOR_TYPE_TO_SWAGGER.keys())}"
                    + " are the accepted monitor types."
                )
        if risk_category_types is not None:
            try:
                swagger_risk_types = [
                    RISK_CATEGORY_TO_SWAGGER[r] for r in risk_category_types
                ]
            except KeyError as e:
                raise ValueError(
                    f"{e.args[0]} is not a valid risk category type,"
                    + f" {list(RISK_CATEGORY_TO_SWAGGER.keys())}"
                    + " are the accepted risk category types."
                )
        project_id = self._get_firewall().project_id.uuid
        api = swagger_client.MonitorServiceApi(self._api_client)
        next_page_token = ""
        has_more = True
        while has_more:
            kwargs: Dict[str, Any] = {}
            if len(next_page_token) > 0:
                kwargs["page_token"] = next_page_token
            else:
                kwargs["first_page_req_included_monitor_types"] = swagger_monitor_types
                kwargs[
                    "first_page_req_included_risk_category_types"
                ] = swagger_risk_types
            with RESTErrorHandler():
                res = api.monitor_service_list_monitors(
                    firewall_id_uuid=self._firewall_id,
                    **kwargs,
                )
            for monitor in res.monitors:
                yield Monitor(
                    self._api_client, monitor.id.uuid, self._firewall_id, project_id
                )
            next_page_token = res.next_page_token
            has_more = res.has_more

    @deprecated(
        "Firewall class methods will not be supported from Robust Intelligence v2.4."
    )
    def start_continuous_test(
        self,
        eval_data_id: str,
        override_existing_bins: bool = False,
        agent_id: Optional[str] = None,
        ram_request_megabytes: Optional[int] = None,
        cpu_request_millicores: Optional[int] = None,
        random_seed: Optional[int] = None,
        rime_managed_image: Optional[str] = None,
        custom_image: Optional[RuntimeinfoCustomImage] = None,
        **exp_fields: Dict[str, object],
    ) -> ContinuousTestJob:
        """Start a Continuous Testing run.

        **Note that the Firewall is deprecated in Robust Intelligence v2.2 and
        will not be supported from v2.4. This method will be replaced by
        `start_continuous_test` in the new ContinuousTest class.**

        Runs a Continuous Testing job on a batch of data.

        Arguments:
            eval_data_id: str
                ID of the evaluation data.
            override_existing_bins: bool
                Specifies whether to override existing bins.
            ram_request_megabytes: Optional[int]
                Megabytes of RAM set as the Kubernetes pod limit for the Stress Test
                Job. The default is 4000MB.
            cpu_request_millicores: Optional[int]
                Millicores of CPU set as the Kubernetes pod limit for the Stress Test
                Job. The default is 1500mi.
            random_seed: Optional[int]
                Random seed to use for the Job, so that Test Job result will be
                deterministic.
            agent_id: Optional[str]
                ID for the Agent where the Continuous Test will be run.
                Uses the default Agent for the workspace when not specified.
            rime_managed_image: Optional[str]
                Name of a Managed Image to use when running the model test.
                The image must have all dependencies required by your model. To create
                new Managed Images with your desired dependencies, use the client's
                `create_managed_image()` method.
            custom_image: Optional[RuntimeinfoCustomImage]
                Specification of a customized container image to use running the model
                test. The image must have all dependencies required by your model.
                The image must specify a name for the image and optionally a pull secret
                (of type RuntimeinfoCustomImagePullSecret) with the name of the
                kubernetes pull secret used to access the given image.
            exp_fields: Dict[str, object]
                Fields for experimental features.

        Returns:
            ContinuousTestJob:
                A ``Job`` object corresponding to the model Continuous Test Job.

        Raises:
            ValueError
                This error is generated when the request to the ModelTesting service
                fails.

        Example:
            .. code-block:: python

                firewall = project.get_firewall()
                eval_data_id = client.register_dataset("example dataset", data_config)
                job = firewall.start_continuous_test(
                    eval_data_id=eval_data_id,
                    ram_request_megabytes=8000,
                    cpu_request_millicores=2000,
                )
        """
        if ram_request_megabytes is not None and ram_request_megabytes <= 0:
            raise ValueError(
                "The requested number of megabytes of RAM must be positive"
            )

        if cpu_request_millicores is not None and cpu_request_millicores <= 0:
            raise ValueError(
                "The requested number of millicores of CPU must be positive"
            )

        req = ContinuoustestsFirewallIdUuidBody(
            test_run_incremental_config=TestrunTestRunIncrementalConfig(
                eval_dataset_id=eval_data_id,
                run_time_info=RuntimeinfoRunTimeInfo(
                    resource_request=RuntimeinfoResourceRequest(
                        ram_request_megabytes=ram_request_megabytes,
                        cpu_request_millicores=cpu_request_millicores,
                    ),
                    random_seed=random_seed,
                ),
            ),
            override_existing_bins=override_existing_bins,
            experimental_fields=exp_fields if exp_fields else None,
            agent_id=RimeUUID(agent_id) if agent_id else None,
        )
        if custom_image:
            req.test_run_incremental_config.run_time_info.custom_image = (
                RuntimeinfoCustomImageType(custom_image=custom_image)
            )
        if rime_managed_image:
            req.test_run_incremental_config.run_time_info.custom_image = (
                RuntimeinfoCustomImageType(managed_image_name=rime_managed_image)
            )
        with RESTErrorHandler():
            Firewall._throttler.throttle(
                throttling_msg="Your request is throttled to limit # of model tests."
            )
            api = swagger_client.ModelTestingApi(self._api_client)
            job: RimeJobMetadata = api.model_testing_start_continuous_test(
                body=req,
                firewall_id_uuid=self._firewall_id,
            ).job
        return ContinuousTestJob(self._api_client, job.job_id)

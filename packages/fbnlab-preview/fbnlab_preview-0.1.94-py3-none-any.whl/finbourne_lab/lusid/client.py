import uuid

import lusid


class LusidClient:

    def __init__(self, **kwargs):

        api_factory = lusid.utilities.ApiClientFactory(**kwargs)

        self.aggregation_api = api_factory.build(lusid.api.AggregationApi)
        self.allocations_api = api_factory.build(lusid.api.AllocationsApi)
        self.app_metadata_api = api_factory.build(lusid.api.ApplicationMetadataApi)
        self.complex_market_data_api = api_factory.build(lusid.api.ComplexMarketDataApi)
        self.configuration_recipe_api = api_factory.build(lusid.api.ConfigurationRecipeApi)
        self.corp_action_source_api = api_factory.build(lusid.api.CorporateActionSourcesApi)
        self.cut_label_definition_api = api_factory.build(lusid.api.CutLabelDefinitionsApi)
        self.data_types_api = api_factory.build(lusid.api.DataTypesApi)
        self.derived_txn_portfolios_api = api_factory.build(lusid.api.DerivedTransactionPortfoliosApi)
        self.entities_api = api_factory.build(lusid.api.EntitiesApi)
        self.instruments_api = api_factory.build(lusid.api.InstrumentsApi)
        self.legal_entities_api = api_factory.build(lusid.api.LegalEntitiesApi)
        self.orders_api = api_factory.build(lusid.api.OrdersApi)
        self.persons_api = api_factory.build(lusid.api.PersonsApi)
        self.portfolio_groups_api = api_factory.build(lusid.api.PortfolioGroupsApi)
        self.portfolios_api = api_factory.build(lusid.api.PortfoliosApi)
        self.property_defs_api = api_factory.build(lusid.api.PropertyDefinitionsApi)
        self.quotes_api = api_factory.build(lusid.api.QuotesApi)
        self.reconciliations_api = api_factory.build(lusid.api.ReconciliationsApi)
        self.reference_portfolios_api = api_factory.build(lusid.api.ReferencePortfolioApi)
        self.scopes_api = api_factory.build(lusid.api.ScopesApi)
        self.search_api = api_factory.build(lusid.api.SearchApi)
        self.sequences_api = api_factory.build(lusid.api.SequencesApi)
        self.strucured_results_api = api_factory.build(lusid.api.StructuredResultDataApi)
        self.system_config_api = api_factory.build(lusid.api.SystemConfigurationApi)
        self.transaction_portfolios_api = api_factory.build(lusid.api.TransactionPortfoliosApi)

    def ensure_portfolio(self, scope, code_prefix, effective_date):
        """

        Args:
            scope:
            code_prefix:
            effective_date:

        Returns:

        """

        def make_portfolio_code(prefix):
            return f"portfolio-{prefix}-{uuid.uuid4()}"

        code = make_portfolio_code(code_prefix)

        import lusid.models as models
        from lusid.exceptions import ApiException

        try:
            self.portfolios_api.get_portfolio(scope, code)

        except ApiException as e:

            transactions_portfolio_request = models.CreateTransactionPortfolioRequest(
                display_name="test portfolio",
                code=code,
                base_currency="GBP",
                created=effective_date
            )
            self.transaction_portfolios_api.create_portfolio(
                scope,
                create_transaction_portfolio_request=transactions_portfolio_request
            )

        return code

    def ensure_property_definitions(self, n_props, scope, domain):
        """ Check whether the desired number of propery definitions exist in a specific scope and domain.
        If not, create them.

        Args:
            n_props: number of property definitions to check
            scope: scope of the property definitions
            domain: domain where the property definitions are

        Returns:
            True if the property definitions exist or been successfully created.
            False if there is failure while creating property definitions.
                The unsuccessfully created property definitions will be printed to the terminal.

        """

        import lusid.models as models
        from lusid.exceptions import ApiException
        
        for i in range(n_props):
            try:
                self.property_defs_api.get_property_definition(
                    domain=domain,
                    scope=scope,
                    code=f"test_prop{i}"
                )
            except ApiException as e:
                # property definition doesn't exist (returns 404), so create one
                property_definition = models.CreatePropertyDefinitionRequest(
                    domain=domain,
                    scope=scope,
                    life_time="Perpetual",
                    code=f"test_prop{i}",
                    value_required=False,
                    data_type_id=models.ResourceId("system", "number"),
                    display_name="test_property"
                )
                # create the property
                self.property_defs_api.create_property_definition(create_property_definition_request=property_definition)

        failed_request = []
        for i in range(n_props):
            try:
                self.property_defs_api.get_property_definition(
                    domain=domain,
                    scope=scope,
                    code=f"test_prop{i}"
                )
            except ApiException as e:
                failed_request.append(f"{domain}/{scope}/test_prop{i}")

        if len(failed_request) > 0:
            print('Creating property definitions was unsuccessful:\n')
            print("\n".join(failed_request))
            return False

        return True

    def ensure_instruments(self, n_insts, id_prefix, properties=None):
        """

        Args:
            n_insts:
            id_prefix:
            properties:

        Returns:

        """

        if properties is None:
            properties = []

        import lusid.models as models
        instruments = {
            f'inst_{i}': models.InstrumentDefinition(
                name=f'Instrument{i}',
                identifiers={"ClientInternal": models.InstrumentIdValue(f'{id_prefix}_{i}')},
                properties=properties
            )
            for i in range(n_insts)
        }

        self.instruments_api.upsert_instruments(request_body=instruments)

    def delete_scope(self, scope):
        """

        Args:
            scope:

        Returns:

        """

        vals = self.portfolios_api.list_portfolios_for_scope(scope=scope).values
        pf_ids = [v.id for v in vals]
        for pf_id in pf_ids:
            self.portfolios_api.delete_portfolio(pf_id.scope, pf_id.code)

    @staticmethod
    def build_properties(n_props, scope, domain):
        """ Build a number of property objects for a certain scope and domain.

        Args:
            n_props: number of properties to build
            scope: scope where the properties wil be created
            domain: domain of the entity the properties belong
        Returns:
            list of property objects
        """
        import lusid.models as models
        properties = [
            models.ModelProperty(
                key=f'{domain}/{scope}/test_prop{i}',
                value=lusid.PropertyValue(metric_value=models.MetricValue(value=i * 100))
            )
            for i in range(n_props)
        ]
        return properties

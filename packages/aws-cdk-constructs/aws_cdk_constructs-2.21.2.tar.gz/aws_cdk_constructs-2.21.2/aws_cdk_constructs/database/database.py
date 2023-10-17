import aws_cdk as cdk
import aws_cdk.aws_s3
from constructs import Construct
from aws_cdk import (
    aws_rds as _rds,
    aws_ec2 as _ec2,
    aws_kms as _kms,
    aws_route53 as route53,
    aws_cloudwatch as _cloudwatch,
    aws_iam as _iam,
)
from aws_cdk_constructs.utils import (
    normalize_environment_parameter,
    get_version,
)
from typing import Union, List

engine_to_cdk_engine = {
    'legacy-aurora-mysql': _rds.DatabaseClusterEngine.aurora,
    'aurora-mysql': _rds.DatabaseClusterEngine.aurora_mysql,
    'aurora-postgresql': _rds.DatabaseClusterEngine.aurora_postgres,
    'aurora-postgresql-12': _rds.DatabaseClusterEngine.aurora_postgres,
    'oracle_s2': _rds.DatabaseInstanceEngine.oracle_se2,
    'oracle_ee': _rds.DatabaseInstanceEngine.oracle_ee,
    'mysql': _rds.DatabaseInstanceEngine.mysql,
    'postgresql': _rds.DatabaseInstanceEngine.postgres,
    'sqlserver-se': _rds.DatabaseInstanceEngine.sql_server_se,
    'sqlserver-ex': _rds.DatabaseInstanceEngine.sql_server_ex,
}

engine_to_cluster_parameter_group_family = {
    'legacy-aurora-mysql': 'default.aurora5.6',
    'aurora-mysql': 'default.aurora-mysql5.7',
    'aurora-postgresql': 'default.aurora-postgresql9.6',
    'aurora-postgresql-12': 'default.aurora-postgresql12',
    'oracle_s2': 'default.oracle-se2-19',
    'oracle_ee': 'default.oracle-ee-19',
    'mysql': 'default.mysql5.7',
    'postgresql': None,
    'sqlserver-se': 'default.sqlserver-se-14.0',
    'sqlserver-ex': 'default.sqlserver-ex-14.0',
}

engine_to_version_class = {
    'legacy-aurora-mysql': _rds.AuroraEngineVersion,
    'aurora-mysql': _rds.AuroraMysqlEngineVersion,
    'mysql': _rds.MysqlEngineVersion,
    'oracle_s2': _rds.OracleEngineVersion,
    'oracle_ee': _rds.OracleEngineVersion,
    'aurora-postgresql': _rds.AuroraPostgresEngineVersion,
    'aurora-postgresql-12': _rds.AuroraPostgresEngineVersion,
    'postgresql': _rds.PostgresEngineVersion,
    'sqlserver-se': _rds.SqlServerEngineVersion,
    'sqlserver-ex': _rds.SqlServerEngineVersion,
}


class Database(Construct):
    """
    The FAO CDK Database Construct is used to create RDS databases.

    The construct automatically enables the following main features:

    -	Compatible with every RDS engine and version;
    -	Create a pre-populated database from RDS snapshots;
    -	Implement High Availability for production databases;
    -	Enable access to the FAO SMTP servers if the databases need to send email notifications (additional configuration at the database level may be required);
    -	Automatic backups and retention configuration according to FAO standards;
    -	Access from the Production Control bastion host server;
    -	Database admin user created using AWS Secret Manager, with password rotation enabled every 30 days;
    -	Encryption at rest of the database storage;
    -	Default or custom RDS parameter group setup;
    -	Adoption of the official database naming convention defined by the CSI database admin team;
    -	Conditionally configure the database removal policy depending on the environment in which the construct is deployed. The policy will be set as `RETAIN` for the Production environment, otherwise set to `DESTROY`;
    -	Conditionally enablement of the deletion protection setup for Production databases;
    -	Private DNS record creation for non-Production environments;
    -	Native integration with the FAO Instance Scheduler to automatically control the uptime of the database;
    -	Conditionally set the license model of Oracle databases;
    -	Enable access from Oracle OEM for Oracle database;
    -	Conditionally export Audit logs to CloudWatch;
    -	Conditionally grant permission to export data to a specified AWS S3 Bucket;
    -	Conditionally tracking of database metrics in the FAO CloudWatch dashboard;

    Every resource created by the construct will be tagged according to the FAO AWS tagging strategy described at https://aws.fao.org

    Args:

        id (str): the logical id of the newly created resource

        app_name (str): The application name. This will be used to generate the 'ApplicationName' tag for CSI compliance. The ID of the application. This must be unique for each system, as it will be used to calculate the AWS costs of the system

        environment (str): Specify the environment in which you want to deploy you system. Allowed values: Development, QA, Production, SharedServices

        environments_parameters (dict): The dictionary containing the references to CSI AWS environments. This will simplify the environment promotions and enable a parametric development of the infrastructures.

        database_instance_type (str):

        database_name (str): Default=fao_default_schema The main database schema name (for 'Production' environment this must be 'fao_default_schema')

        database_master_username (str): Default="faoadmin" the database admin account username (for 'Production' environment this must be 'faoadmin')

        database_snapshot_id (str): The ARN of the Database Snapshot to restore. The snapshot contains the data that will be inserted into the database. Note that if specified, "DatabaseName" parameter will be ignored.

        database_engine (str): The engine of database you want to create

        database_engine_version (str | DatabaseClusterEngine): The engine version of database you want to create. Leave blank to get the latest version of the selected database engine (MySQL 5.7, PostgreSQL 10). More info https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-engineversion

        database_cluster_parameters_group_name (str):  The name of the DB cluster parameter group to associate with this DB cluster. This parameter depends on the Database Engine version you previously selected. In case you leave blank the version use default.aurora-mysql5.7 or default.aurora-postgresql10. If this argument is omitted, default.aurora5.6 is used. If default.aurora5.6 is used, specifying aurora-mysql or aurora-postgresql for the Engine property might result in an error. More info https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-engineversion

        database_identifier_postfix (str):  An optional RDS database identifier postfix. If not provided the Database instance name will follow the pattern: `app_name` + "-" + `environment` + "-"+ `database_engine`. If provided it will be `app_name` + "-" + `postfix` + "-" + `environment` + "-"+ `database_engine`.

        parameter_group (aws_rds.ParameterGroup): The parameter group to assign to the database

        option_group (aws_rds.OptionGroup): The option group to assign to the database

        database_allocated_storage (str): The size of the allocated space for the database. This is GB

        database_will_send_email (str): If the database should send email

        tag_scheduler_uptime (str): specifies the time range in which the AWS resource should be kept up and running - format `HH:mm-HH:mm` (i.e. 'start'-'end'), where the 'start' time must be before 'end'

        tag_scheduler_uptime_days (str): weekdays in which the `SchedulerUptime` tag should be enforced. If not specified, `SchedulerUptime` will be enforced during each day of the week - format integer from 1 to 7, where 1 is Monday

        tag_scheduler_uptime_skip (str): to skip optimization check - format Boolean (`true`, `false`)

        character_set_name (str):  For supported engines, specifies the character set to associate with the DB instance (Not applicable to Aurora Cluster)

        oracle_license_is_byol (str):  Applicable only to Oracle instances. The default license model is LICENSE_INCLUDED, specify this param in case you want to have an Oracle BRING_YOUR_OWN_LICENSE licence model

        s3_export_buckets (Optional[Sequence[IBucket]]): S3 buckets that you want to load data into. This feature is only supported by the Aurora database engine. This property must not be used if s3ExportRole is used. For MySQL: Default: - None

        s3_import_buckets (Optional[Sequence[IBucket]]): S3 buckets that you want to load data from. This feature is only supported by the Aurora database engine. This property must not be used if s3ImportRole is used. For MySQL: Default: - None

        rubrik_backup (str): to enable/disable Rubrik backup using tag `RubrikBackup` - format Boolean (`true`, `false`). Default: true

        cloudwatch_audit_log (str): Applicable only to Oracle instances. If to enable audit logs export in S3. The default is no log exports. Specify this param in case you want to have the audit log export enabled

        dns_record: (Optional | str) The DNS record associated to the Database if multiple Databases

        create_dns: (Optional | str) to enable/disable dns creation - format Boolean (`true`, `false`). Default: true


    """

    @property
    def security_group(self) -> _ec2.SecurityGroup:
        """Return the database security group

        Returns:
            aws_ec2.SecurityGroup: the database security group
        """
        return self._rds_security_group

    @property
    def cluster(self) -> _rds.DatabaseCluster:
        """Return the database cluster

        Returns:
            aws_rds.DatabaseCluster: the database cluster
        """
        return self._cluster

    @property
    def instance(self) -> _rds.DatabaseInstance:
        """Return the database instance

        Returns:
            aws_rds.DatabaseInstance: the database instance
        """
        return self._instance

    @staticmethod
    def get_engine(
        database_engine: str, database_engine_version: str
    ) -> Union[_rds.DatabaseClusterEngine, _rds.DatabaseInstanceEngine]:
        """Return the database engine as string

        Returns:
            str: the database engine as string
        """
        # For MySQL engine: extract db major version
        major_version = database_engine_version.split('.')
        major_version = major_version[:-1]
        major_version = '.'.join(major_version)

        return engine_to_cdk_engine[database_engine](
            # version=database_engine_version if database_engine_version else None
            version=engine_to_version_class[database_engine].of(
                database_engine_version, major_version
            )
        )

    def __init__(
        self,
        scope: Construct,
        id: str,
        app_name: str,
        environment: str,
        environments_parameters: dict,
        database_instance_type: str = None,
        database_name: str = None,
        database_master_username: str = 'faoadmin',
        database_snapshot_id: str = None,
        database_engine: str = None,
        database_engine_version: Union[str, _rds.DatabaseClusterEngine] = None,
        database_cluster_parameters_group_name: str = None,
        database_identifier_postfix: str = '',
        parameter_group: _rds.ParameterGroup = None,
        option_group: _rds.OptionGroup = None,
        database_allocated_storage: str = None,
        database_will_send_email: bool = False,
        tag_scheduler_uptime: str = '',
        tag_scheduler_uptime_days: str = '',
        tag_scheduler_uptime_skip: str = '',
        character_set_name: str = None,
        oracle_license_is_byol: str = None,
        s3_export_buckets: List[aws_cdk.aws_s3.Bucket] = None,
        s3_import_buckets: List[aws_cdk.aws_s3.Bucket] = None,
        rubrik_backup: str = 'True',
        cloudwatch_audit_log: str = None,
        dns_record: str = None,
        create_dns: str = 'True',
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)
        self.scope = scope
        self.app_name = app_name
        self._id = id
        self.dashboard = None
        environment = normalize_environment_parameter(environment)
        app_name = app_name.lower().strip()

        # Apply mandatory tags
        cdk.Tags.of(self).add('ApplicationName', app_name)
        cdk.Tags.of(self).add('Environment', environment)

        # Apply FAO CDK tags
        cdk.Tags.of(self).add('fao-cdk-construct', 'database')
        cdk.Tags.of(cdk.Stack.of(self)).add('fao-cdk-version', get_version())
        cdk.Tags.of(cdk.Stack.of(self)).add('fao-cdk', 'true')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create conditions

        environment = environment.lower()
        aws_account = environments_parameters['accounts'][environment]
        account_id = aws_account['id']
        vpc = _ec2.Vpc.from_vpc_attributes(
            self,
            'VPC',
            vpc_id=aws_account['vpc'],
            public_subnet_ids=aws_account['public_subnet_ids'],
            private_subnet_ids=aws_account['private_subnet_ids'],
            availability_zones=aws_account['availability_zones'],
        )

        is_production = environment == 'production'
        is_not_production = not is_production

        is_ha = is_production

        use_snapshot = database_snapshot_id

        is_cluster_compatible = 'aurora' in database_engine
        is_not_cluster_compatible = not is_cluster_compatible

        is_oracle = 'oracle' in database_engine
        is_sqlserver = 'sqlserver' in database_engine
        is_sqlserver_ex = 'sqlserver-ex' in database_engine

        has_no_parameter_group = (
            parameter_group is None
            and database_cluster_parameters_group_name is None
        )
        has_no_defult_parameter_group = (
            has_no_parameter_group
            and engine_to_cluster_parameter_group_family[database_engine]
            is None
        )

        has_no_option_group = option_group is None

        sends_emails = (
            database_will_send_email
            and isinstance(database_will_send_email, str)
            and database_will_send_email.lower() == 'true'
        )

        self._instance = None
        self._cluster = None
        self._rds_security_group = None

        to_be_backed_up = (
            rubrik_backup
            and isinstance(rubrik_backup, str)
            and rubrik_backup.lower() == 'true'
        )

        identifier_postfix = (
            f'-{database_identifier_postfix}'
            if database_identifier_postfix
            else ''
        )
        output_id = f'{app_name}{identifier_postfix}-{environment}-'
        database_identifier = output_id.replace('_', '-')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CloudFormation outputs
        cdk.CfnOutput(
            self, f'DatabaseAppName{app_name}{output_id}', value=str(app_name)
        )
        cdk.CfnOutput(
            self, f'DatabaseIsHa{app_name}{output_id}', value=str(is_ha)
        )
        cdk.CfnOutput(
            self,
            f'DatabaseEngine{app_name}{output_id}',
            value=str(database_engine),
        )
        cdk.CfnOutput(
            self,
            f'DatabaseEngineVersion{app_name}{output_id}',
            value=str(database_engine_version),
        )
        # cdk.CfnOutput(self, f"DatabaseAllocatedStorage{app_name}{output_id}", value=str(database_allocated_storage))
        cdk.CfnOutput(
            self,
            f'DatabaseWillSendEmail{app_name}{output_id}',
            value=str(sends_emails),
        )
        cdk.CfnOutput(
            self,
            f'DatabaseHasBackup{app_name}{output_id}',
            value=str(to_be_backed_up),
        )
        cdk.CfnOutput(
            self,
            f'DatabaseName{app_name}{output_id}',
            value=str(database_name),
        )
        cdk.CfnOutput(
            self,
            f'DatabaseIdentifierPrefix{app_name}{output_id}',
            value=str(database_identifier),
        )

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Validate input params

        # TODO

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Retrieve info from already existing AWS resources
        # Important: you need an internet connection!

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create AWS resources

        # ~~~~~~~~~~~~~~~~
        # Security group
        # ~~~~~~~~~~~~~~~~
        self._rds_security_group = _ec2.SecurityGroup(
            self,
            'rds_sg',
            vpc=vpc,
            security_group_name=app_name + self._id + 'rds_sg',
            allow_all_outbound=True,
        )

        bastion_host_production_control_security_group = (
            _ec2.SecurityGroup.from_security_group_id(
                self,
                'bastion_host_production_control_security_group',
                aws_account['bastion_host_production_control_security_group'],
                mutable=False,
            )
        )

        security_groups = [
            self._rds_security_group,
            bastion_host_production_control_security_group,
        ]

        # Security group to send email
        if sends_emails:
            smtp_access_security_group = (
                _ec2.SecurityGroup.from_security_group_id(
                    self,
                    'smtp_relay_security_group',
                    aws_account['smtp_relay_security_group'],
                    mutable=False,
                )
            )
            security_groups.append(smtp_access_security_group)

        # ~~~~~~~~~~~~~~~~
        # RDS Instance type
        # ~~~~~~~~~~~~~~~~
        instance_type = _ec2.InstanceType(database_instance_type)
        instance_props = _rds.InstanceProps(
            instance_type=instance_type,
            vpc=vpc,
            security_groups=security_groups,
        )

        # ~~~~~~~~~~~~~~~~
        # AWS Secret Manager
        # ~~~~~~~~~~~~~~~~
        credentials = _rds.Credentials.from_username(database_master_username)

        # ~~~~~~~~~~~~~~~~
        # KMS Encryption key
        # ~~~~~~~~~~~~~~~~
        # SQL Server Express does not support encryption
        if not is_sqlserver_ex:
            key_arn = (
                'arn:aws:kms:eu-west-1:'
                + account_id
                + ':key/'
                + aws_account['kms_rds_key']
            )
            encryption_key = _kms.Key.from_key_arn(
                self, 'encryption_key', key_arn
            )
        else:
            encryption_key = None

        # ~~~~~~~~~~~~~~~~
        # RDS Parameter group
        # ~~~~~~~~~~~~~~~~
        my_parameter_group = None
        if has_no_defult_parameter_group is False:
            my_parameter_group = (
                parameter_group
                or _rds.ParameterGroup.from_parameter_group_name(
                    self,
                    'parameter_group',
                    parameter_group_name=database_cluster_parameters_group_name
                    if database_cluster_parameters_group_name
                    else engine_to_cluster_parameter_group_family[
                        database_engine
                    ],
                )
            )

        # ~~~~~~~~~~~~~~~~
        # RDS Database engine
        # ~~~~~~~~~~~~~~~~
        self._engine = (
            (self.get_engine(database_engine, database_engine_version))
            if isinstance(database_engine_version, str)
            else database_engine_version
        )

        # ~~~~~~~~~~~~~~~~
        # RDS Cluster
        # ~~~~~~~~~~~~~~~~
        if is_cluster_compatible:
            self._cluster = _rds.DatabaseCluster(
                self,
                'cluster',
                engine=self._engine,
                instance_props=instance_props,
                credentials=credentials,
                cluster_identifier=database_identifier + database_engine,
                instance_identifier_base=database_identifier,
                deletion_protection=is_production,
                # No need to create instance resource, only specify the amount
                instances=2 if is_ha else 1,
                backup=_rds.BackupProps(
                    retention=cdk.Duration.days(30),
                    preferred_window='01:00-02:00',
                ),
                default_database_name='fao_default_schema',
                preferred_maintenance_window='mon:03:00-mon:04:00',
                parameter_group=my_parameter_group,
                storage_encryption_key=encryption_key,
                s3_export_buckets=s3_export_buckets,
                s3_import_buckets=s3_import_buckets,
            )

            self._cluster.add_rotation_single_user(
                automatically_after=cdk.Duration.days(30)
            )
            if not is_production and create_dns.lower() == 'true':
                # Create DNS record
                cluster_hostname = str(self._cluster.cluster_endpoint.hostname)
                cluster_hostname = ''.join(cluster_hostname.split())

                hosted_zone_id = aws_account['route53_hosted_zone_id']
                domain_name = aws_account['route53_domain_name']

                dns_record = 'db.' + app_name if app_name else dns_record
                dns_record = (
                    dns_record + '-' + database_identifier_postfix
                    if database_identifier_postfix
                    else dns_record
                )
                route53_zone = (
                    route53.PrivateHostedZone.from_hosted_zone_attributes(
                        self,
                        f'RDSPrivateHostedZone{dns_record}',
                        hosted_zone_id=hosted_zone_id,
                        zone_name=domain_name,
                    )
                )
                route53.CnameRecord(
                    self,
                    f'RDSAliasRecord{dns_record}',
                    zone=route53_zone,
                    # target=cdk.Token.as_string(self._cluster.cluster_endpoint), # << Not working here
                    # target=route53.RecordTarget.from_values(self._cluster.cluster_endpoint.hostname),
                    domain_name=cluster_hostname,
                    record_name=f'{dns_record}.{domain_name}',
                )

            # Conditionally create a cluster from a snapshot
            if use_snapshot:
                self._cluster.node.find_child(
                    'Resource'
                ).add_property_override(
                    'SnapshotIdentifier', database_snapshot_id
                )
                # While creating an RDS from a snapshot, MasterUsername cannot be specified
                self._cluster.node.find_child(
                    'Resource'
                ).add_property_override('MasterUsername', None)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FAO AWS Scheduler tags
            if is_not_production:
                clus = self._cluster.node.find_child('Resource')
                instance = self._cluster.node.find_child('Instance1')

                if tag_scheduler_uptime_skip:
                    cdk.Tags.of(clus).add(
                        'SchedulerSkip', tag_scheduler_uptime_skip
                    )
                    cdk.Tags.of(instance).add(
                        'SchedulerSkip', tag_scheduler_uptime_skip
                    )

                if tag_scheduler_uptime:
                    cdk.Tags.of(clus).add(
                        'SchedulerUptime', tag_scheduler_uptime
                    )
                    cdk.Tags.of(instance).add(
                        'SchedulerUptime', tag_scheduler_uptime
                    )

                if tag_scheduler_uptime_days:
                    cdk.Tags.of(clus).add(
                        'SchedulerUptimeDays', tag_scheduler_uptime_days
                    )
                    cdk.Tags.of(instance).add(
                        'SchedulerUptimeDays', tag_scheduler_uptime_days
                    )

        # ~~~~~~~~~~~~~~~~
        # RDS Instance
        # ~~~~~~~~~~~~~~~~
        if is_not_cluster_compatible:

            # Default RDS license model is NONE
            license_model = None
            # Default RDS cloudwatch logs export in NONE
            cloudwatch_logs_exports = None

            if is_oracle:

                # Default Oracle license model is LICENSE_INCLUDED
                license_model = _rds.LicenseModel.LICENSE_INCLUDED

                oracle_oem_client_security_group = (
                    _ec2.SecurityGroup.from_security_group_id(
                        self,
                        'oracle_oem_client_security_group',
                        aws_account['oracle_oem_client_security_group'],
                        mutable=False,
                    )
                )
                security_groups.append(oracle_oem_client_security_group)

                should_be_byol_oracle_license_model = (
                    oracle_license_is_byol
                    and isinstance(oracle_license_is_byol, str)
                    and oracle_license_is_byol.lower() == 'true'
                )

                if should_be_byol_oracle_license_model:
                    # If user specified change to BRING_YOUR_OWN_LICENSE
                    license_model = _rds.LicenseModel.BRING_YOUR_OWN_LICENSE

                should_be_cloudwatch_audit_log = (
                    cloudwatch_audit_log
                    and isinstance(cloudwatch_audit_log, str)
                    and cloudwatch_audit_log.lower() == 'true'
                )

                if should_be_cloudwatch_audit_log:
                    # If user specified change to cloud watch log setting
                    cloudwatch_logs_exports = _rds.cloudwatch_logs_exports = [
                        'audit'
                    ]

            if is_sqlserver:
                # Default SQL server license model is LICENSE_INCLUDED
                license_model = _rds.LicenseModel.LICENSE_INCLUDED

            if is_sqlserver_ex or not is_production:
                is_multi_az = False
            else:
                is_multi_az = True

            self._instance = _rds.DatabaseInstance(
                self,
                'instance',
                engine=self._engine,
                allocated_storage=database_allocated_storage
                and int(database_allocated_storage),
                allow_major_version_upgrade=False,
                database_name=database_name if database_name else None,
                license_model=license_model,
                credentials=credentials,
                parameter_group=my_parameter_group,
                instance_type=instance_type,
                vpc=vpc,
                auto_minor_version_upgrade=True,
                backup_retention=cdk.Duration.days(30),
                copy_tags_to_snapshot=True,
                deletion_protection=is_production,
                instance_identifier=database_identifier + 'db',
                # max_allocated_storage=None,
                multi_az=is_multi_az,
                option_group=None if has_no_option_group else option_group,
                preferred_maintenance_window='mon:03:00-mon:04:00',
                processor_features=None,
                security_groups=security_groups,
                storage_encryption_key=encryption_key,
                character_set_name=character_set_name,
                cloudwatch_logs_exports=cloudwatch_logs_exports,
                s3_export_buckets=s3_export_buckets,
                s3_import_buckets=s3_import_buckets,
            )

            if s3_export_buckets or s3_import_buckets:
                # This fix is required to enable SQL server integration with S3.
                # Default CDK generated permissions are not enough
                s3_import_policy = (
                    self._instance.node.find_child('S3ImportRole')
                    .node.find_child('DefaultPolicy')
                    .node.default_child
                )
                rds_s3_list_statement = _iam.PolicyStatement(
                    actions=['s3:ListAllMyBuckets'],
                    resources=['*'],
                )
                s3_import_policy.policy_document.add_statements(
                    rds_s3_list_statement
                )

            # Conditionally create an instance from a snapshot
            if use_snapshot:
                self._instance.node.find_child(
                    'Resource'
                ).add_property_override(
                    'DBSnapshotIdentifier', database_snapshot_id
                )
                # While creating an RDS from a snapshot, MasterUsername cannot be specified
                self._instance.node.find_child(
                    'Resource'
                ).add_property_override('MasterUsername', None)

            self._instance.add_rotation_single_user(
                automatically_after=cdk.Duration.days(30)
            )

            # Create DNS record
            if not is_production:
                instance_hostname = str(
                    self._instance.instance_endpoint.hostname
                )
                instance_hostname = ''.join(instance_hostname.split())

                hosted_zone_id = aws_account['route53_hosted_zone_id']
                domain_name = aws_account['route53_domain_name']

                dns_record = 'db.' + app_name if app_name else dns_record
                dns_record = (
                    dns_record + '-' + database_identifier_postfix
                    if database_identifier_postfix
                    else dns_record
                )
                route53_zone = (
                    route53.PrivateHostedZone.from_hosted_zone_attributes(
                        self,
                        f'RDSPrivateHostedZone{dns_record}',
                        hosted_zone_id=hosted_zone_id,
                        zone_name=domain_name,
                    )
                )
                route53.CnameRecord(
                    self,
                    f'RDSAliasRecord{dns_record}',
                    zone=route53_zone,
                    domain_name=instance_hostname,
                    record_name=f'{dns_record}.{domain_name}',
                )

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FAO AWS Rubrik backup tag

            if to_be_backed_up:
                cdk.Tags.of(self._instance).add('RubrikBackup', 'true')
            else:
                cdk.Tags.of(self._instance).add('RubrikBackup', 'false')

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FAO AWS Scheduler tags
            if is_not_production:
                instance = self._instance.node.find_child('Resource')
                if tag_scheduler_uptime_skip:
                    cdk.Tags.of(instance).add(
                        'SchedulerSkip', tag_scheduler_uptime_skip
                    )

                if tag_scheduler_uptime:
                    cdk.Tags.of(instance).add(
                        'SchedulerUptime', tag_scheduler_uptime
                    )

                if tag_scheduler_uptime_days:
                    cdk.Tags.of(instance).add(
                        'SchedulerUptimeDays', tag_scheduler_uptime_days
                    )

    def _get_dashboard(self) -> _cloudwatch.Dashboard:
        path = '_'.join(self.node.path.split('/')[:-1])
        return (
            self.scope.node.try_find_child(f'{self.app_name}-{path}-dashboard')
            or self._create_dashboard()
        )

    def _create_dashboard(self) -> _cloudwatch.Dashboard:
        path = '_'.join(self.node.path.split('/')[:-1])
        return _cloudwatch.Dashboard(
            self.scope,
            f'{self.app_name}-{path}-dashboard',
            dashboard_name=f'{self.app_name}-{path}',
            end='end',
            period_override=_cloudwatch.PeriodOverride.AUTO,
            start='start',
        )

    def render_widgets(self) -> None:
        path = '_'.join(self.node.path.split('/')[:-1])
        self.dashboard = self._get_dashboard()

        if self._cluster:
            self.dashboard.add_widgets(
                _cloudwatch.TextWidget(
                    markdown=f'# {self._id} {path}', width=24
                ),
                _cloudwatch.GraphWidget(
                    left=[self._cluster.metric_cpu_utilization()],
                    title='CPU Utilization',
                ),
                _cloudwatch.GraphWidget(
                    left=[self._cluster.metric_database_connections()],
                    title='DB connections',
                ),
                _cloudwatch.GraphWidget(
                    left=[self._cluster.metric_free_local_storage()],
                    title='Free local storage',
                ),
                _cloudwatch.GraphWidget(
                    left=[
                        self._cluster.metric_network_receive_throughput(),
                        self._cluster.metric_network_transmit_throughput(),
                    ],
                    title='Network throughput',
                ),
            )
        else:
            self.dashboard.add_widgets(
                _cloudwatch.TextWidget(
                    markdown=f'# {self._id} {path}', width=24
                ),
                _cloudwatch.GraphWidget(
                    left=[self._instance.metric_cpu_utilization()],
                    title='CPU Utilization',
                ),
                _cloudwatch.GraphWidget(
                    left=[self._instance.metric_database_connections()],
                    title='DB connections',
                ),
                _cloudwatch.GraphWidget(
                    left=[self._instance.metric_free_storage_space()],
                    title='Free local storage',
                ),
            )

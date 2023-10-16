from time import sleep

from lumipy.client import Client
from lumipy.lumiflex._atlas.utils import process_direct_provider_metadata, process_data_provider_metadata

data_providers_sql = '''
    -- atlas build - data provider query

    @x = SELECT
      COALESCE([Description], 'Not available') as [Description], 
      [Category], 
      COALESCE([DocumentationLink], 'Not available') as [DocumentationLink], 
      [Type], 
      [Name] AS [TableName], 
      [Attributes] AS [ProvAttributes], 
      [NamespaceLevel]
    FROM
      [Sys.Registration]
    WHERE
      [Type] = 'DataProvider'
      and [Name] NOT LIKE '%@%'
    GROUP BY
      [Name];

    @data_prov_meta = SELECT 
        * 
    FROM 
        @x
    WHERE
        [TableName] REGEXP '^[A-Za-z0-9_\-\.]+$';

    @data_prov_flds = SELECT
      [FieldName], [TableName], [DataType], [FieldType], [IsMain], [IsPrimaryKey], 
      COALESCE([ParamDefaultValue], 'None') as [ParamDefaultValue], 
      COALESCE([TableParamColumns], 'No schema') as [TableParamColumns], 
      COALESCE([Description], 'Not available') AS [Description_fld], 
      COALESCE([AllowedValues], 'Any') as [AllowedValues], 
      [ConditionUsage], 
      COALESCE([SampleValues], 'None available') as [SampleValues]
    FROM
      [Sys.Field]
    WHERE
      [TableName] IN (SELECT
      [TableName]
    FROM
      @data_prov_meta);

    SELECT
      svc.[Description], svc.[Category], svc.[DocumentationLink], fld.[FieldName], fld.[DataType], fld.[FieldType], 
      fld.[IsMain], fld.[IsPrimaryKey], fld.[ParamDefaultValue], fld.[TableParamColumns], 
      fld.[Description_fld], svc.[TableName] AS [TableName], svc.[Type],
      fld.[AllowedValues], fld.[ConditionUsage], fld.[SampleValues],
      svc.[ProvAttributes], svc.[NamespaceLevel]
    FROM
      @data_prov_meta AS svc 
      LEFT JOIN
    @data_prov_flds AS fld
        ON svc.[TableName] = fld.[TableName]
    WHERE
        fld.[FieldName] IS NOT NULL
    '''

# noinspection SqlNoDataSourceInspection,SqlResolve
direct_providers_sql = '''
    -- atlas build - direct provider query

    SELECT
      COALESCE([Description], 'Not available') as [Description], 
      COALESCE([DocumentationLink], 'Not available') as [DocumentationLink], 
      [Type], 
      [Category], 
      [Name] as TableName, 
      [CustomSyntax],
      [Attributes] AS [ProvAttributes], 
      [NamespaceLevel]
    FROM
      Sys.Registration
    WHERE
      [Type] = 'DirectProvider'
      and [Name] NOT IN ('Tools.Pivot', 'Tools.Unpivot', 'Sys.Admin.SetupView')
      and [Name] NOT LIKE 'Sql.Db%'
      and [CustomSyntax] IS NOT NULL
      and [Name] NOT LIKE '%@%'
    GROUP BY
      [Name]
    ORDER BY
      [Name] ASC
    '''


def atlas_queries(c: Client):

    j1 = c.run(data_providers_sql, quiet=True, return_job=True)
    j2 = c.run(direct_providers_sql, quiet=True, return_job=True)

    def spinning_globe():
        while True:
            strs = ['Getting Atlas🌏','\r', 'Getting Atlas🌍', '\r', 'Getting Atlas🌎', '\r']
            for s in strs:
                yield s

    globes = spinning_globe()
    while j1.is_running() or j2.is_running():
        print(next(globes), end='')
        sleep(0.1)
    print()

    data_df = process_data_provider_metadata(j1.get_result(quiet=True))
    direct_df = process_direct_provider_metadata(j2.get_result(quiet=True))

    return data_df, direct_df

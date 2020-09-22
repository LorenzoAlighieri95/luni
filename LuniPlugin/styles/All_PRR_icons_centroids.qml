<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" maxScale="0" version="3.10.3-A Coruña" labelsEnabled="0" simplifyAlgorithm="0" minScale="1e+08" readOnly="0" styleCategories="AllStyleCategories" simplifyDrawingHints="0" simplifyLocal="1" simplifyDrawingTol="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="RuleRenderer" enableorderby="0" forceraster="0" symbollevels="0">
    <rules key="{ed4494c3-a166-4748-ba32-5949214e7530}">
      <rule filter="prob>=70 and (ruolo ='arcipretura' or ruolo = 'pieve' or ruolo = 'rettoria' or ruolo = 'prioria')" key="{34063fc7-bdea-4e82-8230-745fd7bf4a12}" symbol="0" label="Chiesa grande > 70%"/>
      <rule filter="prob&lt;70 and prob>=40 and (ruolo ='arcipretura' or ruolo = 'pieve' or ruolo = 'rettoria' or ruolo = 'prioria')" key="{1e4c7170-3efa-4248-b889-a247282fc93d}" symbol="1" label="Chiesa grande &lt; 70%"/>
      <rule filter="prob>10 and prob&lt;40 and (ruolo ='arcipretura' or ruolo = 'pieve' or ruolo = 'rettoria' or ruolo = 'prioria')" key="{172fa775-45f8-4456-a513-3c73db36ac84}" symbol="2" label="Chiesa grande &lt; 40%"/>
      <rule filter="prob>=70 and (ruolo = 'cappella' or ruolo = 'chiesa' or ruolo= 'oratorio')" key="{9e353e58-395f-40fb-8f03-79f8cf4bbbe3}" symbol="3" label="Chiesa piccola > 70%"/>
      <rule filter="prob&lt;70 and prob>=40 and (ruolo = ' cappella' or ruolo = 'chiesa' or ruolo= 'oratorio')" key="{2bbe1bc5-fc3c-400c-841a-da02b90f33b5}" symbol="4" label="Chiesa piccola &lt; 70%"/>
      <rule filter="prob>10 and prob &lt;40 and (ruolo = ' cappella' or ruolo = 'chiesa' or ruolo= 'oratorio')" key="{33746453-026a-4424-86e4-1d2848941cb7}" symbol="5" label="Chiesa piccola &lt; 40%"/>
      <rule filter="prob >= 70 and ruolo = 'ospedale'" key="{c58eb838-9d07-412c-8d74-daa6f55b457d}" symbol="6" label="Ospedale > 70%"/>
      <rule filter="prob&lt; 70 and prob >= 40 and ruolo = 'ospedale'" key="{8af5d1d7-a607-47db-b939-3e7e0cb9ed2f}" symbol="7" label="Ospedale &lt; 70%"/>
      <rule filter="prob> 10 and prob &lt; 40 and ruolo = 'ospedale'" key="{4199eb6c-dd2b-4302-8048-4f7ffb945d05}" symbol="8" label="Ospedale &lt; 40%"/>
      <rule filter="prob >= 70 and (ruolo = 'monastero' or ruolo = 'convento')" key="{038d868b-40be-47d8-ab74-ecac9215f6ea}" symbol="9" label="Monastero > 70%"/>
      <rule filter="prob &lt; 70 and prob >= 40  and (ruolo = 'monastero' or ruolo = 'convento')" key="{9d3b8361-418c-4d59-8b22-1c3abfbec19a}" symbol="10" label="Monastero &lt; 70%"/>
      <rule filter="prob >10 and prob &lt; 40  and (ruolo = 'monastero' or ruolo = 'convento')" key="{256b50a3-3e3c-4529-a2e9-21bc32fc216d}" symbol="11" label="Monastero &lt; 40%"/>
      <rule filter="prob &lt;=10" key="{fa05f2ab-5325-4d0d-9472-20051eedfe64}" label="Ignoto"/>
    </rules>
    <symbols>
      <symbol type="marker" name="0" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" class="SvgMarker" locked="0" pass="0">
          <prop v="0" k="angle"/>
          <prop v="114,155,111,255" k="color"/>
          <prop v="0" k="fixedAspectRatio"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bigChurch_V.svg" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="7" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="marker" name="1" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" class="SvgMarker" locked="0" pass="0">
          <prop v="0" k="angle"/>
          <prop v="213,180,60,255" k="color"/>
          <prop v="0" k="fixedAspectRatio"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bigChurch_A.svg" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="7" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="marker" name="10" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" class="SvgMarker" locked="0" pass="0">
          <prop v="0" k="angle"/>
          <prop v="152,125,183,255" k="color"/>
          <prop v="0" k="fixedAspectRatio"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="mon_A.svg" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="7" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="marker" name="11" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" class="SvgMarker" locked="0" pass="0">
          <prop v="0" k="angle"/>
          <prop v="231,113,72,255" k="color"/>
          <prop v="0" k="fixedAspectRatio"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="mon_R.svg" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="7" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="marker" name="2" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" class="SvgMarker" locked="0" pass="0">
          <prop v="0" k="angle"/>
          <prop v="164,113,88,255" k="color"/>
          <prop v="0" k="fixedAspectRatio"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bigChurch_R.svg" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="7" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="marker" name="3" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" class="SvgMarker" locked="0" pass="0">
          <prop v="0" k="angle"/>
          <prop v="133,182,111,255" k="color"/>
          <prop v="0" k="fixedAspectRatio"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="littleChurch_V.svg" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="7" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="marker" name="4" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" class="SvgMarker" locked="0" pass="0">
          <prop v="0" k="angle"/>
          <prop v="125,139,143,255" k="color"/>
          <prop v="0" k="fixedAspectRatio"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="littleChurch_A.svg" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="7" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="marker" name="5" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" class="SvgMarker" locked="0" pass="0">
          <prop v="0" k="angle"/>
          <prop v="145,82,45,255" k="color"/>
          <prop v="0" k="fixedAspectRatio"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="littleChurch_R.svg" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="7" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="marker" name="6" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" class="SvgMarker" locked="0" pass="0">
          <prop v="0" k="angle"/>
          <prop v="190,178,151,255" k="color"/>
          <prop v="0" k="fixedAspectRatio"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="hospital_V.svg" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="7" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="marker" name="7" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" class="SvgMarker" locked="0" pass="0">
          <prop v="0" k="angle"/>
          <prop v="229,182,54,255" k="color"/>
          <prop v="0" k="fixedAspectRatio"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="hospital_A.svg" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="7" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="marker" name="8" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" class="SvgMarker" locked="0" pass="0">
          <prop v="0" k="angle"/>
          <prop v="225,89,137,255" k="color"/>
          <prop v="0" k="fixedAspectRatio"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="hospital_R.svg" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="7" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="marker" name="9" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" class="SvgMarker" locked="0" pass="0">
          <prop v="0" k="angle"/>
          <prop v="190,207,80,255" k="color"/>
          <prop v="0" k="fixedAspectRatio"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="mon_V.svg" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="7" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <customproperties>
    <property value="DESCR" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory diagramOrientation="Up" maxScaleDenominator="1e+08" labelPlacementMethod="XHeight" scaleBasedVisibility="0" penColor="#000000" height="15" minimumSize="0" penWidth="0" lineSizeScale="3x:0,0,0,0,0,0" barWidth="5" width="15" sizeType="MM" sizeScale="3x:0,0,0,0,0,0" minScaleDenominator="0" scaleDependency="Area" lineSizeType="MM" backgroundColor="#ffffff" penAlpha="255" opacity="1" enabled="0" backgroundAlpha="255" rotationOffset="270">
      <fontProperties style="" description="MS Shell Dlg 2,7.8,-1,5,50,0,0,0,0,0"/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings zIndex="0" showAll="1" linePlacementFlags="18" placement="0" obstacle="0" dist="0" priority="0">
    <properties>
      <Option type="Map">
        <Option value="" type="QString" name="name"/>
        <Option name="properties"/>
        <Option value="collection" type="QString" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="ID">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="IDENT">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="DESCR">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="MEO">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="MEC">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="TOPON">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ESIST">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="COMUN">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="BIBLI">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="NOTE">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="prob">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ruolo">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="probRuolo">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="ID"/>
    <alias name="" index="1" field="IDENT"/>
    <alias name="" index="2" field="DESCR"/>
    <alias name="" index="3" field="MEO"/>
    <alias name="" index="4" field="MEC"/>
    <alias name="" index="5" field="TOPON"/>
    <alias name="" index="6" field="ESIST"/>
    <alias name="" index="7" field="COMUN"/>
    <alias name="" index="8" field="BIBLI"/>
    <alias name="" index="9" field="NOTE"/>
    <alias name="" index="10" field="prob"/>
    <alias name="" index="11" field="ruolo"/>
    <alias name="" index="12" field="probRuolo"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="ID" expression=""/>
    <default applyOnUpdate="0" field="IDENT" expression=""/>
    <default applyOnUpdate="0" field="DESCR" expression=""/>
    <default applyOnUpdate="0" field="MEO" expression=""/>
    <default applyOnUpdate="0" field="MEC" expression=""/>
    <default applyOnUpdate="0" field="TOPON" expression=""/>
    <default applyOnUpdate="0" field="ESIST" expression=""/>
    <default applyOnUpdate="0" field="COMUN" expression=""/>
    <default applyOnUpdate="0" field="BIBLI" expression=""/>
    <default applyOnUpdate="0" field="NOTE" expression=""/>
    <default applyOnUpdate="0" field="prob" expression=""/>
    <default applyOnUpdate="0" field="ruolo" expression=""/>
    <default applyOnUpdate="0" field="probRuolo" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" constraints="0" field="ID" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="IDENT" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="DESCR" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="MEO" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="MEC" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="TOPON" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="ESIST" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="COMUN" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="BIBLI" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="NOTE" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="prob" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="ruolo" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="probRuolo" exp_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="ID"/>
    <constraint desc="" exp="" field="IDENT"/>
    <constraint desc="" exp="" field="DESCR"/>
    <constraint desc="" exp="" field="MEO"/>
    <constraint desc="" exp="" field="MEC"/>
    <constraint desc="" exp="" field="TOPON"/>
    <constraint desc="" exp="" field="ESIST"/>
    <constraint desc="" exp="" field="COMUN"/>
    <constraint desc="" exp="" field="BIBLI"/>
    <constraint desc="" exp="" field="NOTE"/>
    <constraint desc="" exp="" field="prob"/>
    <constraint desc="" exp="" field="ruolo"/>
    <constraint desc="" exp="" field="probRuolo"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="" sortOrder="0">
    <columns>
      <column type="field" name="ID" hidden="0" width="-1"/>
      <column type="field" name="IDENT" hidden="0" width="-1"/>
      <column type="field" name="DESCR" hidden="0" width="-1"/>
      <column type="field" name="MEO" hidden="0" width="-1"/>
      <column type="field" name="MEC" hidden="0" width="-1"/>
      <column type="field" name="TOPON" hidden="0" width="-1"/>
      <column type="field" name="ESIST" hidden="0" width="-1"/>
      <column type="field" name="COMUN" hidden="0" width="-1"/>
      <column type="field" name="BIBLI" hidden="0" width="-1"/>
      <column type="field" name="NOTE" hidden="0" width="-1"/>
      <column type="field" name="prob" hidden="0" width="-1"/>
      <column type="field" name="ruolo" hidden="0" width="-1"/>
      <column type="field" name="probRuolo" hidden="0" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="1" name="BIBLI"/>
    <field editable="1" name="COMUN"/>
    <field editable="1" name="DESCR"/>
    <field editable="1" name="ESIST"/>
    <field editable="1" name="ID"/>
    <field editable="1" name="IDENT"/>
    <field editable="1" name="MEC"/>
    <field editable="1" name="MEO"/>
    <field editable="1" name="NOTE"/>
    <field editable="1" name="TOPON"/>
    <field editable="1" name="prob"/>
    <field editable="1" name="probRuolo"/>
    <field editable="1" name="ruolo"/>
  </editable>
  <labelOnTop>
    <field name="BIBLI" labelOnTop="0"/>
    <field name="COMUN" labelOnTop="0"/>
    <field name="DESCR" labelOnTop="0"/>
    <field name="ESIST" labelOnTop="0"/>
    <field name="ID" labelOnTop="0"/>
    <field name="IDENT" labelOnTop="0"/>
    <field name="MEC" labelOnTop="0"/>
    <field name="MEO" labelOnTop="0"/>
    <field name="NOTE" labelOnTop="0"/>
    <field name="TOPON" labelOnTop="0"/>
    <field name="prob" labelOnTop="0"/>
    <field name="probRuolo" labelOnTop="0"/>
    <field name="ruolo" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>IDENT</previewExpression>
  <mapTip>&#xd;
&lt;style>&#xd;
.t {color: black; font-size:20px;}&#xd;
&lt;/style>&#xd;
&#xd;
&lt;span class="t">[% "ID" %] - [% "IDENT" %] &lt;/span></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>

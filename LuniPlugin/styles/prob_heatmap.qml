<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyAlgorithm="0" styleCategories="AllStyleCategories" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyDrawingHints="0" simplifyDrawingTol="1" maxScale="0" version="3.10.3-A Coruña" readOnly="0" labelsEnabled="0" simplifyLocal="1" minScale="1e+08">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 weight_expression="prob" enableorderby="0" quality="2" forceraster="0" radius_unit="0" radius_map_unit_scale="3x:0,0,0,0,0,0" type="heatmapRenderer" radius="20" max_value="0">
    <colorramp name="[source]" type="gradient">
      <prop v="255,67,57,0" k="color1"/>
      <prop v="54,160,54,153" k="color2"/>
      <prop v="0" k="discrete"/>
      <prop v="gradient" k="rampType"/>
      <prop v="0.175121;254,76,76,64:0.357488;240,124,0,101" k="stops"/>
    </colorramp>
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
    <DiagramCategory penAlpha="255" penWidth="0" enabled="0" barWidth="5" scaleBasedVisibility="0" lineSizeScale="3x:0,0,0,0,0,0" minimumSize="0" minScaleDenominator="0" sizeScale="3x:0,0,0,0,0,0" height="15" lineSizeType="MM" labelPlacementMethod="XHeight" width="15" scaleDependency="Area" backgroundColor="#ffffff" opacity="1" rotationOffset="270" penColor="#000000" sizeType="MM" maxScaleDenominator="1e+08" backgroundAlpha="255" diagramOrientation="Up">
      <fontProperties description="MS Shell Dlg 2,7.8,-1,5,50,0,0,0,0,0" style=""/>
      <attribute color="#000000" field="" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="0" obstacle="0" zIndex="0" priority="0" showAll="1" linePlacementFlags="18" dist="0">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
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
    <default applyOnUpdate="0" expression="" field="ID"/>
    <default applyOnUpdate="0" expression="" field="IDENT"/>
    <default applyOnUpdate="0" expression="" field="DESCR"/>
    <default applyOnUpdate="0" expression="" field="MEO"/>
    <default applyOnUpdate="0" expression="" field="MEC"/>
    <default applyOnUpdate="0" expression="" field="TOPON"/>
    <default applyOnUpdate="0" expression="" field="ESIST"/>
    <default applyOnUpdate="0" expression="" field="COMUN"/>
    <default applyOnUpdate="0" expression="" field="BIBLI"/>
    <default applyOnUpdate="0" expression="" field="NOTE"/>
    <default applyOnUpdate="0" expression="" field="prob"/>
    <default applyOnUpdate="0" expression="" field="ruolo"/>
    <default applyOnUpdate="0" expression="" field="probRuolo"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="ID"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="IDENT"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="DESCR"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="MEO"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="MEC"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="TOPON"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="ESIST"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="COMUN"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="BIBLI"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="NOTE"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="prob"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="ruolo"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="probRuolo"/>
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
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column name="ID" hidden="0" width="-1" type="field"/>
      <column name="IDENT" hidden="0" width="-1" type="field"/>
      <column name="DESCR" hidden="0" width="-1" type="field"/>
      <column name="MEO" hidden="0" width="-1" type="field"/>
      <column name="MEC" hidden="0" width="-1" type="field"/>
      <column name="TOPON" hidden="0" width="-1" type="field"/>
      <column name="ESIST" hidden="0" width="-1" type="field"/>
      <column name="COMUN" hidden="0" width="-1" type="field"/>
      <column name="BIBLI" hidden="0" width="-1" type="field"/>
      <column name="NOTE" hidden="0" width="-1" type="field"/>
      <column name="prob" hidden="0" width="-1" type="field"/>
      <column name="ruolo" hidden="0" width="-1" type="field"/>
      <column name="probRuolo" hidden="0" width="-1" type="field"/>
      <column hidden="1" width="-1" type="actions"/>
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
    <field name="BIBLI" editable="1"/>
    <field name="COMUN" editable="1"/>
    <field name="DESCR" editable="1"/>
    <field name="ESIST" editable="1"/>
    <field name="ID" editable="1"/>
    <field name="IDENT" editable="1"/>
    <field name="MEC" editable="1"/>
    <field name="MEO" editable="1"/>
    <field name="NOTE" editable="1"/>
    <field name="TOPON" editable="1"/>
    <field name="prob" editable="1"/>
    <field name="probRuolo" editable="1"/>
    <field name="ruolo" editable="1"/>
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
  <previewExpression>DESCR</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>

import React, { useState } from "react";

import { Col, Row, Slider, Typography } from "antd";

import SiderLayout from "../../components/sider-layout/SiderLayout";
import LineGraph from "../../components/graphs/LineGraph";

import { data_bar } from "../../js/data";
import texts from "../../js/texts";

import "./Gallery.css";

export default function Gallery(props) {
  const [numCols, setNumCols]  = useState(3);
  const text = texts.gallery.content.siderLayout;
  return (
    <>
      <SiderLayout 
        title={text.title}
        description={text.description}
        sections={text.sections}
      />
      <div className="ecosystem-breakdown">
        <Row className="ecosystem-breakdown-header" justify="left">
          <Col offset={1} span={18}>
            <Typography.Title level={4}>Ecosystem Breakdown</Typography.Title>
          </Col>
          <Col className="column-slider" span={3}>
            Number of Columns
            <Slider
              min={2}
              max={4}
              value={numCols}
              onChange={setNumCols}
              marks={{2:2, 3:3, 4:4}}
              step={null}
            />
          </Col>
        </Row>
        <Row gutter={[32, 32]} justify="left">
          {data_bar["Contributor"]["male_female"]["x_categories"].slice(1).map(
            (ecosystem, index) => {
              return (<Col span={Math.round(22/numCols)} offset={index%numCols==0 ? 1:0}>
                <LineGraph category={"Contributor"} ecosystem={ecosystem}/>
              </Col>);
            }
          )}
        </Row>
      </div>
    </>
  );
}
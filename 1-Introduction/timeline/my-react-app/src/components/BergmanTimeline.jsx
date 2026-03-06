import React from "react";
import {
  VerticalTimeline,
  VerticalTimelineElement
} from "react-vertical-timeline-component";
import "react-vertical-timeline-component/style.min.css";
import bergmanEvents from "../data/bergmanEvents";

const BergmanTimeline = () => {
  return (
    <div>
      <h2 style={{textAlign: "center", margin: "1rem 0"}}>Ingmar Bergman — Timeline</h2>
      <VerticalTimeline>
        {bergmanEvents.map(ev => (
          <VerticalTimelineElement
            key={ev.id}
            date={ev.date}
            iconStyle={{
              background: ev.type === "film" ? "#8b0000" : "#2e6da4",
              color: "#fff"
            }}
            contentStyle={{ boxShadow: "0 3px 10px rgba(0,0,0,0.2)" }}
          >
            <h3 className="vertical-timeline-element-title">{ev.title}</h3>
            <p style={{whiteSpace: "pre-line"}}>{ev.description}</p>
            {ev.image ? <img src={ev.image} alt={ev.title} style={{maxWidth: "200px", marginTop: "8px"}}/> : null}
          </VerticalTimelineElement>
        ))}
      </VerticalTimeline>
    </div>
  );
};

export default BergmanTimeline;

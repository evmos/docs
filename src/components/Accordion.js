import React from "react";

const Accordion = ({title, body}) => {
    return (
        <details>
            <summary>{title}</summary>
            {body}
        </details>
    )
}

const Accordions = ({data}) => {
    const result = data.map((question, i) => <Accordion key={i} title={question.title} body={question.body} />);
    return result;
}

export default Accordions;
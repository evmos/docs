import React from "react";
import ProjectValue from "./ProjectValue";
import './styles.css';

const Highlighter = ({pretext='', keyword, postText=''}) => {
    return <span className="highlighter">{pretext}<ProjectValue keyword={keyword} />{postText}</span>
}

export default Highlighter;
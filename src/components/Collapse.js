import React from 'react';
import Details from '@theme/MDXComponents/Details';

export default function Collapse (props) {
    const { children, title } = props;

    return (
        <Details>
            <summary mdxType="summary">{title}</summary>

            {children}
        </Details>
    );
}
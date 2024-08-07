import React from 'react';
import SearchBar from '@theme-original/SearchBar';
import AskCookbook from '@cookbookdev/docsbot/react'
import BrowserOnly from '@docusaurus/BrowserOnly';

/** It's a public API key, so it's safe to expose it here */
const COOKBOOK_PUBLIC_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NmIyNTY3ZDM3ZWIwYzRiMTVlYWE1YjIiLCJpYXQiOjE3MjI5NjM1ODEsImV4cCI6MjAzODUzOTU4MX0.vpVV5fCo1WcnruoFu1XKxYWY5ewzSfYvzLkoJYjojD4";

export default function SearchBarWrapper(props) {
  return (
    <>
      <SearchBar {...props} />
      <BrowserOnly>{() => <AskCookbook apiKey={COOKBOOK_PUBLIC_API_KEY} />}</BrowserOnly>
    </>
  );
}

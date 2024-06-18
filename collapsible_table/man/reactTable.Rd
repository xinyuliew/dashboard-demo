% Auto-generated: do not edit by hand
\name{reactTable}

\alias{reactTable}

\title{ReactTable component}

\description{

}

\usage{
reactTable(id=NULL, rows=NULL)
}

\arguments{
\item{id}{Character. }

\item{rows}{List of lists containing elements 'id', 'date', 'text', 'stance', 'sentiment', 'num_replies', 'replies'.
those elements have the following types:
  - id (character; required)
  - date (character; required)
  - text (character; required)
  - stance (character; required)
  - sentiment (character; required)
  - num_replies (numeric; required)
  - replies (optional): . replies has the following type: list of lists containing elements 'id', 'date', 'text', 'stance', 'sentiment', 'num_replies', 'replies'.
those elements have the following types:
  - id (character; required)
  - date (character; required)
  - text (character; required)
  - stance (character; required)
  - sentiment (character; required)
  - num_replies (numeric; required)
  - replies (unnamed list; optional)ss. }
}

\value{named list of JSON elements corresponding to React.js properties and their values}


# AUTO GENERATED FILE - DO NOT EDIT

#' @export
reactTable <- function(id=NULL, rows=NULL) {
    
    props <- list(id=id, rows=rows)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'ReactTable',
        namespace = 'collapsible_table',
        propNames = c('id', 'rows'),
        package = 'collapsibleTable'
        )

    structure(component, class = c('dash_component', 'list'))
}

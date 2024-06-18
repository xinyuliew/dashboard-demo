import React, { useState } from 'react';
import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import Collapse from '@mui/material/Collapse';
import IconButton from '@mui/material/IconButton';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import TablePagination from '@mui/material/TablePagination';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import Button from '@mui/material/Button';

function Row(props) {
    const { row, openRows, handleToggle, depth } = props;
    const isOpen = openRows[row.id];

    const renderNestedReplies = () => {
        if (row.num_replies === 0 || !isOpen) {
            return null;
        }

        return (
            <TableRow>
                <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
                    <Collapse in={isOpen} timeout="auto" unmountOnExit>
                        <Box margin={1}>
                            <Table size="small" aria-label="nested replies">
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Date</TableCell>
                                        <TableCell>Text</TableCell>
                                        <TableCell>Stance</TableCell>
                                        <TableCell>Sentiment</TableCell>
                                        <TableCell>No. of replies</TableCell>
                                        <TableCell>Expand</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {row.replies.map((reply) => (
                                        <Row key={reply.id} row={reply} openRows={openRows} handleToggle={handleToggle} depth={depth + 1} />
                                    ))}
                                </TableBody>
                            </Table>
                        </Box>
                    </Collapse>
                </TableCell>
            </TableRow>
        );
    };

    return (
        <React.Fragment>
            <TableRow className="tableRow">
                <TableCell className="dateCell">{row.date}</TableCell>
                <TableCell className="textCell">{row.text}</TableCell>
                <TableCell className="stanceCell">{row.stance}</TableCell>
                <TableCell className="sentimentCell">{row.sentiment}</TableCell>
                <TableCell className="numRepliesCell">{row.num_replies}</TableCell>
                <TableCell className="toggleCell">
                    {row.num_replies > 0 && (
                        <IconButton
                            aria-label={isOpen ? 'collapse row' : 'expand row'}
                            size="small"
                            onClick={() => handleToggle(row.id)}
                            className="toggleButton"
                        >
                            {isOpen ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                        </IconButton>
                    )}
                </TableCell>
            </TableRow>
            {renderNestedReplies()}
        </React.Fragment>
    );
}

Row.propTypes = {
    row: PropTypes.shape({
        id: PropTypes.string.isRequired,
        date: PropTypes.string.isRequired,
        text: PropTypes.string.isRequired,
        stance: PropTypes.string.isRequired,
        sentiment: PropTypes.string.isRequired,
        num_replies: PropTypes.number.isRequired,
        replies: PropTypes.arrayOf(
            PropTypes.shape({
                id: PropTypes.string.isRequired,
                date: PropTypes.string.isRequired,
                text: PropTypes.string.isRequired,
                stance: PropTypes.string.isRequired,
                sentiment: PropTypes.string.isRequired,
                num_replies: PropTypes.number.isRequired,
                replies: PropTypes.array,
            })
        ),
    }).isRequired,
    openRows: PropTypes.object.isRequired,
    handleToggle: PropTypes.func.isRequired,
    depth: PropTypes.number.isRequired,
};

const ReactTable = (props) => {
    const { rows } = props;
    const [openRows, setOpenRows] = useState({});
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);
    const [searchTerm, setSearchTerm] = useState('');
    const [filterStance, setFilterStance] = useState('');
    const [filterSentiment, setFilterSentiment] = useState('');

    const handleToggle = (id) => {
        setOpenRows((prevOpenRows) => ({
            ...prevOpenRows,
            [id]: !prevOpenRows[id],
        }));
    };

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    const handleSearch = (event) => {
        setSearchTerm(event.target.value);
    };

    const handleFilterStance = (event) => {
        setFilterStance(event.target.value);
    };

    const handleFilterSentiment = (event) => {
        setFilterSentiment(event.target.value);
    };

    const clearAllFilters = () => {
        setSearchTerm('');
        setFilterStance('');
        setFilterSentiment('');
    };

    const filteredRows = rows.filter(row => {
        const textMatches = row.text.toLowerCase().includes(searchTerm.toLowerCase());
        const stanceMatches = !filterStance || row.stance.toLowerCase() === filterStance.toLowerCase();
        const sentimentMatches = !filterSentiment || row.sentiment.toLowerCase() === filterSentiment.toLowerCase();
        return textMatches && stanceMatches && sentimentMatches;
    });

    const paginatedRows = filteredRows.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);

    const expandedRows = paginatedRows.map((row, index) => ({
        ...row,
        id: (page * rowsPerPage + index).toString(), // Ensure each row has a unique id as a string
        replies: row.replies && row.replies.map((reply, replyIndex) => ({
            ...reply,
            id: `${page * rowsPerPage + index}-${replyIndex}`, // Ensure each reply has a unique id
        })),
    }));

    return (
        <TableContainer component={Paper}>
            <Box display="flex" justifyContent="flex-end" alignItems="center" padding={2}>
                <TextField
                    id="search-bar"
                    label="Search"
                    type="search"
                    variant="outlined"
                    value={searchTerm}
                    onChange={handleSearch}
                    style={{ marginRight: '16px' }}
                />
                <TextField
                    id="filter-stance"
                    select
                    label="Filter Stance"
                    variant="outlined"
                    value={filterStance}
                    onChange={handleFilterStance}
                    style={{ marginRight: '16px', minWidth: '150px' }}
                >
                    <MenuItem value="">All</MenuItem>
                    <MenuItem value="against">Against</MenuItem>
                    <MenuItem value="favor">Favor</MenuItem>
                    <MenuItem value="none">None</MenuItem>
                </TextField>
                <TextField
                    id="filter-sentiment"
                    select
                    label="Filter Sentiment"
                    variant="outlined"
                    value={filterSentiment}
                    onChange={handleFilterSentiment}
                    style={{ marginRight: '16px', minWidth: '150px' }}
                >
                    <MenuItem value="">All</MenuItem>
                    <MenuItem value="positive">Positive</MenuItem>
                    <MenuItem value="neutral">Neutral</MenuItem>
                    <MenuItem value="negative">Negative</MenuItem>
                </TextField>
                <Button variant="contained" color="secondary" onClick={clearAllFilters}>
                    Clear All
                </Button>
            </Box>
            <Table aria-label="collapsible table" className="customTable">
                <TableHead>
                    <TableRow>
                        <TableCell className="dateHeader">Date</TableCell>
                        <TableCell className="textHeader">Text</TableCell>
                        <TableCell className="stanceHeader">Stance</TableCell>
                        <TableCell className="sentimentHeader">Sentiment</TableCell>
                        <TableCell className="numRepliesHeader">No. of replies</TableCell>
                        <TableCell className="toggleHeader">Expand</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {expandedRows.map((row) => (
                        <Row key={row.id} row={row} openRows={openRows} handleToggle={handleToggle} depth={1} />
                    ))}
                </TableBody>
            </Table>
            <TablePagination
                rowsPerPageOptions={[10, 20, 30]}
                component="div"
                count={filteredRows.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
            />
        </TableContainer>
    );
};

ReactTable.propTypes = {
    id: PropTypes.string.isRequired,
    rows: PropTypes.arrayOf(
        PropTypes.shape({
            id: PropTypes.string.isRequired,
            date: PropTypes.string.isRequired,
            text: PropTypes.string.isRequired,
            stance: PropTypes.string.isRequired,
            sentiment: PropTypes.string.isRequired,
            num_replies: PropTypes.number.isRequired,
            replies: PropTypes.arrayOf(
                PropTypes.shape({
                    id: PropTypes.string.isRequired,
                    date: PropTypes.string.isRequired,
                    text: PropTypes.string.isRequired,
                    stance: PropTypes.string.isRequired,
                    sentiment: PropTypes.string.isRequired,
                    num_replies: PropTypes.number.isRequired,
                    replies: PropTypes.array,
                })
            ),
        })
    ).isRequired,
};


export default ReactTable;

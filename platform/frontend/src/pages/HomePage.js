import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
// import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TablePagination from '@material-ui/core/TablePagination';
import TableRow from '@material-ui/core/TableRow';
import Header from "../components/Header";
import Container from '@material-ui/core/Container';
import Footer from "../components/Footer"

import {getContents} from "../services/content.service"

const columns = [
    {id: 'examRef', label: 'Examen Ref',  extract:(row) => {return row.exam.ref}},
    {id: 'examDate', label: 'Examen Date',  extract:(row) => {return row.exam.date}},
    {id: 'examWording', label: 'Examen Wording', extract:(row) => {return row.exam.wording.word}},
    {id: 'examRoom', label: 'Examen Room', extract:(row) => {return row.exam.room.ref}},
];

const useStyles = makeStyles((theme) => ({
    root: {
        width: '100%',
    },
    container: {
        paddingTop: theme.spacing(4),
        paddingBottom: theme.spacing(6),
    },
}));

export default function StickyHeadTable() {
    const classes = useStyles();
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(10);

    const [isLoading, setIsLoading] = React.useState(true);
    const [refreshData, setRefreshData] = React.useState(true);
    const [data, setData] = React.useState(null);

    React.useEffect(() => {
        if (data)
            setIsLoading(false)
        if (refreshData){
            setRefreshData(false)
            getContents('/exam-reports/', {limit:rowsPerPage,offset:page * rowsPerPage,depth:3}, setData)
        }
     }, [data, setData, refreshData, setRefreshData, rowsPerPage, page, setIsLoading]);


    const handleChangePage = (event, newPage) => {
        setPage(newPage)
        setRefreshData(true)
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(event.target.value);
        setPage(0);
        setRefreshData(true);
    }

    const handleDocumentClick = (event) => {
        window.location = "/document/" + event.target.parentElement.id;
    }

    if (isLoading)
       return (<div></div>)

    return (
        <div className={classes.root}>
            <Header></Header>
            {/*<Paper className={classes.root}>*/}

            <Container maxWidth="lg" className={classes.container}>
                <TableContainer className={classes.container}>
                    <Table stickyHeader aria-label="sticky table">
                        <TableHead>
                            <TableRow>
                                {columns.map((column) => (
                                    <TableCell
                                        key={column.id}
                                        align={column.align}
                                        style={{minWidth: column.minWidth}}
                                    >
                                        {column.label}
                                    </TableCell>
                                ))}
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {data.results.map((row) => {
                                return (
                                    <TableRow id={row.id} hover role="checkbox" tabIndex={-1} key={row.id} onClick={handleDocumentClick}>
                                        {columns.map((column) => {
                                            return (
                                                <TableCell key={column.id} align={column.align}>
                                                    {column.extract(row)}
                                                </TableCell>
                                            );
                                        })}
                                    </TableRow>
                                );
                            })}
                        </TableBody>
                    </Table>

                </TableContainer>

                <TablePagination
                    rowsPerPageOptions={[10, 25, 50, 100]}
                    component="div"
                    count={data.count}
                    rowsPerPage={rowsPerPage}
                    page={page}
                    onChangePage={handleChangePage}
                    onChangeRowsPerPage={handleChangeRowsPerPage}
                />
            </Container>

            {/*</Paper>*/}
            <Footer/>
        </div>

    );
}

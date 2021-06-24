import React from 'react';
import PropTypes from 'prop-types';
import {makeStyles} from '@material-ui/core/styles';
import Box from '@material-ui/core/Box';
import IconButton from '@material-ui/core/IconButton';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Typography from '@material-ui/core/Typography';
import KeyboardArrowDownIcon from '@material-ui/icons/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@material-ui/icons/KeyboardArrowUp';
import Header from "../components/Header";
import Container from "@material-ui/core/Container";
import Grid from '@material-ui/core/Grid';
import TextArea from "../components/Text/TextArea"
import Footer from "../components/Footer"
import BoxCheck from '../components/BoxCheck'
import FeaturesTable from '../components/FeaturesTable'
import Progress from "../components/CircularProgress/CircularProgress"
import CloudWord from "../components/Charts/WordCloud"

import {getContents} from "../services/content.service"

const useRowStyles = makeStyles({
    root: {
        '& > *': {
            borderBottom: 'unset',
        },
    },
});

const useStyles = makeStyles((theme) => ({
    root: {
        display: 'flex',
    },
    // appBarSpacer: theme.mixins.toolbar,
    // content: {
    //   flexGrow: 1,
    //   height: '100vh',
    //   overflow: 'auto',
    //   paddingRight: 24,
    // },
    container: {
        paddingTop: theme.spacing(4),
        paddingBottom: theme.spacing(4),
        paddingLeft:theme.spacing(8),
        paddingRight: theme.spacing(8),
    },
    paper: {
        padding: theme.spacing(2),
        display: 'flex',
        overflow: 'auto',
        flexDirection: 'column',
    },
    fixedHeight: {
        height: 240,
    },
}));

function Row(props) {
    const {row} = props;
    const [open, setOpen] = React.useState(false);
    const classes = useRowStyles();

    return (
        <React.Fragment>
            <TableRow className={classes.root}>
                <TableCell>
                    <IconButton aria-label="expand row" size="small" onClick={() => setOpen(!open)}>
                        {open ? <KeyboardArrowUpIcon/> : <KeyboardArrowDownIcon/>}
                    </IconButton>
                </TableCell>
                <TableCell component="th" scope="row">
                    {row.info}
                </TableCell>
                <TableCell align="center">{row.precision}</TableCell>
                <TableCell align="center">{row.résultat}</TableCell>

            </TableRow>
            <TableRow>
                <TableCell style={{paddingBottom: 0, paddingTop: 0}} colSpan={6}>

                    <Box margin={1}>
                        <Typography variant="h6" gutterBottom component="div">
                            Another
                        </Typography>
                        <Table size="small" aria-label="purchases">
                            <TableHead>
                                <TableRow>
                                    <TableCell>Date</TableCell>
                                    <TableCell>Source</TableCell>
                                    <TableCell>Valeur</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {row.Another.map((historyRow) => (
                                    <TableRow key={historyRow.Date}>
                                        <TableCell component="th" scope="row">
                                            <BoxCheck/>
                                            {historyRow.Date}
                                        </TableCell>
                                        <TableCell>
                                            {historyRow.Source}</TableCell>
                                        <TableCell>
                                            {historyRow.Valeur}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </Box>

                </TableCell>
            </TableRow>
        </React.Fragment>
    );
}

Row.propTypes = {
    row: PropTypes.shape({
        precision: PropTypes.number.isRequired,
        résultat: PropTypes.string.isRequired,
        history: PropTypes.arrayOf(
            PropTypes.shape({
                Source: PropTypes.string.isRequired,
                Date: PropTypes.string.isRequired,
                Valeur: PropTypes.number.isRequired,
            }),
        ).isRequired,
        info: PropTypes.string.isRequired,
    }).isRequired,
};


export default function CollapsibleTable({match}) {
    const classes = useStyles();

    const [isLoading, setIsLoading] = React.useState(true);
    const [data, setData] = React.useState(null);

    React.useEffect(() => {
        if (data)
            setIsLoading(false)
        else
            getContents("/exam-reports/" + match.params.id + "/", {depth: 2}, setData)
    }, [match, isLoading, data, setData, setIsLoading]);


    if (isLoading)
        return (<div><Progress/></div>)

    return (
        <div>
            <Header/>

            <Container maxWidth="xl" className={classes.container}>
                <Grid container spacing={6}>
                    <Grid item xs={12} sm={7}>
                        <TextArea text={data.text}/>
                    </Grid>
                    <Grid item xs={12} sm={5}>
                        <FeaturesTable examId={data.id} features={data.features}/>
                        <CloudWord/>
                    </Grid>

                </Grid>
            </Container>


            <Footer/>
        </div>
    );
}

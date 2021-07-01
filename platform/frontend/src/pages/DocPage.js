import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Header from "../components/Header";
import Container from "@material-ui/core/Container";
import Grid from '@material-ui/core/Grid';
import TextArea from "../components/Text/TextArea"
import Footer from "../components/Footer"
import FeaturesTable from '../components/FeaturesTable'
import Progress from "../components/CircularProgress/CircularProgress"
import CloudWord from "../components/Charts/WordCloud"

import {getContents} from "../services/content.service"
import FeatureForm from '../components/FeatureForm';

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

export default function CollapsibleTable({match}) {
    const classes = useStyles();

    const [isLoading, setIsLoading] = React.useState(true);
    const [data, setData] = React.useState(null);

    const [highlight, setHighlight] = React.useState(null)
    const [newFeatureValue, setNewFeatureValue] = React.useState(false)
    const [onEndSelection, setOnEndSelection] = React.useState(() => () => {})

    React.useEffect(() => {
        if (data)
            setIsLoading(false)
        else
            getContents("/exam-reports/" + match.params.id + "/", {depth: 2}, setData)
    }, [match, isLoading, data, setData, setIsLoading]);

    const handleTextSelection = (span, onEndSelection) => {
        setNewFeatureValue(span)
        setOnEndSelection(() => () => onEndSelection())
    }

    const handleAddFeatureEnd = (data) => {
        onEndSelection()
        setNewFeatureValue(false)
        if (data)
            setData(data);
    }

    if (isLoading)
        return (<div><Progress/></div>)

    return (
        <div>
            <Header/>

            <Container maxWidth="xl" className={classes.container}>
                <Grid container spacing={6}>
                    <Grid item xs={12} sm={7}>
                        <TextArea text={data.text} highlight={highlight} onSelectText={handleTextSelection} />
                    </Grid>
                    <Grid item xs={12} sm={5}>
                        <FeaturesTable examId={data.id} features={data.features} 
                        text={data.text} onHighlight={setHighlight} onAddFeature={setNewFeatureValue} onDeleteFeature={setData}/>
                        <CloudWord/>
                    </Grid>

                </Grid>
            </Container>
            <FeatureForm newFeatureValue={newFeatureValue} onAddFeatureEnd={handleAddFeatureEnd} features={data.features} examId={data.id}/>
            <Footer/>
        </div>
    );
}

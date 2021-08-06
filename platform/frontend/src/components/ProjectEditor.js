import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';
import ModelViewer from './ModelViewer';
import Button from '@material-ui/core/Button';
import FormGroup from '@material-ui/core/FormGroup';
import Grid from '@material-ui/core/Grid';
import {getContents, postContent} from "../services/content.service";
import Progress from "../components/CircularProgress/CircularProgress";


const useStyles = makeStyles((theme) => ({
    deleteButton: {
        display: 'flex',
        position: 'absolute',
        right: '32px',
    },
    paper: {
        padding: theme.spacing(2)
    },
    projectTitle: {
        marginTop: '6px'
    },
    controlButtons: {
        marginTop: theme.spacing(2)
    }
    
}));

export default function ProjectEditor(props) {
    const classes = useStyles();

    const [modelInfo, setModelInfo] =  React.useState (null)
    const [isLoading, setIsLoading] =  React.useState (true)

    const {projectData} = props

    const updateModelInfo = React.useCallback((data) => {
        const newData = data.map((element) => {
            const name = element.name
            const desc = element.desc
            const state = projectData.active_models.includes(name)
            return {name, desc, state}
        })
        setModelInfo(newData)
    }, [setModelInfo]);

    React.useEffect(() => {
        if (modelInfo)
            setIsLoading(false)
        else {
            setIsLoading(true)
            getContents('/models-info/', {}, updateModelInfo)
        }
    }, [modelInfo, updateModelInfo, setIsLoading]);

    const handleSave = () => {

    }

    const handleCancel = () => {
        setIsLoading(true)
        setModelInfo(null)
    }
    
    if (isLoading)
        return (<div><Progress/></div>)

    return (
        <Paper className= {classes.paper}>
            <FormGroup row>
                <Typography className= {classes.projectTitle} variant='h5'>
                    {projectData.name} ({projectData.nbDocument} documents)
                </Typography>
                <IconButton className ={classes.deleteButton} color="primary" aria-label="Delete Project">
                    <DeleteIcon ></DeleteIcon>
                </IconButton>
            </FormGroup>
            {modelInfo.map((element, i) => <ModelViewer modelData = {modelInfo[i]}></ModelViewer>)}
            <Grid className= {classes.controlButtons} container direction="row" justifyContent="flex-end" spacing= {2}> 
                <Grid item >
                    <Button onClick={handleCancel} variant="contained" color="secondary">Cancel</Button>
                </Grid>

                <Grid item >
                    <Button onClick={handleSave} variant="contained" color="primary">Save</Button>
                </Grid>
            </Grid>


        </Paper>
        )
}
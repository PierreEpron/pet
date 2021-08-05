import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';
import ModelViewer from './ModelViewer';
import Button from '@material-ui/core/Button';
import FormGroup from '@material-ui/core/FormGroup';



const models = [
    {name:'Pet', state: true, desc: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."},
    {name:'Dim', state: true, desc: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."}
    
]

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
}));

export default function ProjectEditor(props) {
    const classes = useStyles();
    // const [loading, setLoading] = React.useState(false);
    const {projectData} = props
    console.log(projectData)
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
            {models.map((element, i) => <ModelViewer modelData = {models[i]}></ModelViewer>)}
            <Button variant="contained" color="secondary">Cancel</Button>
            <Button variant="contained" color="primary">Save</Button>


        </Paper>
        )
}
import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';
import Switch from '@material-ui/core/Switch';  
import FormControlLabel from '@material-ui/core/FormControlLabel'; 

const useStyles = makeStyles((theme) => ({
     paper: {
        padding: theme.spacing(2)
    }
}));

export default function ModelViewer(props) {
    const classes = useStyles();
    const {modelData} = props;
    const [modelState, setModelState] = React.useState(modelData.state);
    
    console.log(modelData)
    return (
        <Paper className= {classes.paper}>
            <Typography>
                {modelData.name}
            </Typography>
            <FormControlLabel
                control={
                    <Switch
                        checked={modelState}
                        onChange={(e) => setModelState(e.target.checked)}
                        name="modelState"
                        color="primary"
                         />
                }
                label="Active"
            />
            <Typography>
                {modelData.desc}
            </Typography>
        </Paper>
        )
}
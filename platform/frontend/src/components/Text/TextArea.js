import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';

const useStyles = makeStyles((theme) => ({
  root: {
    whiteSpace:"pre-wrap",
    padding:"24px"
  }
}));


export default function MaxHeightTextarea(props) {
  const classes = useStyles();

  return (
    <Paper className={classes.root}>
      {props.text}
    </Paper>
  );
}
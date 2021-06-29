import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import { red } from '@material-ui/core/colors';

const useStyles = makeStyles((theme) => ({
  root: {
    whiteSpace:"pre-wrap",
    padding:"24px"
  },
  highlight: {
    backgroundColor:"red"
  }
}));


export default function MaxHeightTextarea(props) {
  const classes = useStyles();

  const parseText = (text) => {
    console.log('in')
    if (props.highlight) {
      const start = props.highlight[0]
      const end = props.highlight[1]
      return (
        <div>
          <span>{text.substring(0, start)}</span>
          <span className={classes.highlight}>{text.substring(start, end)}</span>
          <span>{text.substring(end, text.length)}</span>
        </div>
      )
      
    } 
    else 
      return <div><span>{text}</span></div>
  }

  return (
    <Paper className={classes.root}>
      {parseText(props.text)}
    </Paper>
  );
}
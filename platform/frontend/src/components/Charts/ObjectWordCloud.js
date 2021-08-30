import React from 'react'
import { TagCloud } from 'react-tagcloud'

export default (props) => {(
  <TagCloud
    minSize={12}
    maxSize={35}
    tags={props.data}
  />
)}
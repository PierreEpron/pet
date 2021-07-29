import React from 'react'
import { TagCloud } from 'react-tagcloud'

const data = [
  { value: 'SuV', count: 25 },
  { value: 'Adénophatie', count: 18 },
  { value: 'Nodules', count: 38 },
  { value: 'Chimio', count: 30 },
  { value: 'Mutliple', count: 28 },
  { value: 'Tep', count: 25 },
  { value: 'Radiothérapie', count: 33 },
  { value: 'Chirurgie', count: 20 },
  { value: 'Localisation', count: 22 },
  { value: 'Hyperfixation', count: 7 },
  { value: 'Hypermetabolisme', count: 25 },
  { value: 'Suv ref', count: 15 },
]

// bring your own implementation of rng
let seed = 1337
function random() {
  const x = Math.sin(seed++) * 10000
  return x - Math.floor(x)
}

export default () => (
  <TagCloud
    minSize={12}
    maxSize={35}
    tags={data}
    randomNumberGenerator={random}
  />
)
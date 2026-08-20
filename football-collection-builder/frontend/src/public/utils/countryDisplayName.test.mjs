import test from 'node:test'
import assert from 'node:assert/strict'
import { countryDisplayName } from './countryDisplayName.ts'

test('normalizes the three public country slugs without changing them',()=>{
 const slugs=['brasil','italia','outros']
 assert.deepEqual(slugs.map(countryDisplayName),['Brasil','Itália','Outros'])
 assert.deepEqual(slugs,['brasil','italia','outros'])
})

test('is case insensitive and keeps a conservative fallback',()=>{
 assert.equal(countryDisplayName('ITALIA'),'Itália')
 assert.equal(countryDisplayName('regiao futura'),'Regiao futura')
})

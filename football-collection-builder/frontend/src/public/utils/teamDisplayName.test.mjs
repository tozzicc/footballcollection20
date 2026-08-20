import test from 'node:test'
import assert from 'node:assert/strict'
import { teamDisplayName } from './teamDisplayName.ts'

test('resolves safe real team names without changing identity inputs',()=>{
 const identity={countrySlug:'brasil',slug:'saopaulo',name:'saopaulo'}
 assert.equal(teamDisplayName(identity),'São Paulo')
 assert.deepEqual(identity,{countrySlug:'brasil',slug:'saopaulo',name:'saopaulo'})
})

test('handles accents, hyphens, prepositions and case-insensitive keys',()=>{
 assert.equal(teamDisplayName('ATLETICO','BRASIL'),'Atlético-MG')
 assert.equal(teamDisplayName('america-mg','brasil'),'América-MG')
 assert.equal(teamDisplayName('vasco','brasil'),'Vasco da Gama')
 assert.equal(teamDisplayName('internaciol-limeira','brasil'),'Internacional de Limeira')
})

test('uses a deterministic conservative fallback',()=>{
 assert.equal(teamDisplayName('clube_exemplo','outros'),'Clube Exemplo')
 assert.equal(teamDisplayName('clube_exemplo','outros'),'Clube Exemplo')
})

test('preserves route slugs while localizing the Italy display only',()=>{
 const slug='italy',route=`/site/paises/italia/equipes/${slug}`
 assert.equal(teamDisplayName(slug,'italia'),'Itália')
 assert.equal(route,'/site/paises/italia/equipes/italy')
})

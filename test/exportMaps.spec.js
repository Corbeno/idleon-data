const sinon = require('sinon')
const fs = require('fs');
const chai = require('chai').expect
const path = require('path')

const maps = require('../src/exportMaps');
const { expect } = require('chai');

const normalizedPath = path.join(__dirname, '../maps');

describe('exportMap', () => {
  
  beforeEach(function () {
    sinon.stub(fs, 'readdirSync')
      .withArgs(normalizedPath)
      .returns(['foo.json', 'README.md', 'bar.json']);
  
    sinon.stub(fs, 'readFileSync')
      .withArgs(path.join(normalizedPath, 'foo.json'), 'utf-8')
      .returns('{"baz": "123", "lmao": true}')
      .withArgs(path.join(normalizedPath, 'bar.json'), 'utf-8')
      .returns('{"mmmmk": "123", "lmao": false}');
    
  })

  it('Includes .json files', () => {
    maps.exportMaps();

    expect(fs.readFileSync.withArgs(path.join(normalizedPath, 'foo.json'), 'utf-8').calledOnce).to.equal(true)
  })

  it('Does not include non-json files', () => {
    maps.exportMaps();

    expect(fs.readFileSync.withArgs(path.join(normalizedPath, 'README.md'), 'utf-8').notCalled).to.equal(true)
  })

  it('Combines multiple .json files', () => {
    const myObj = maps.exportMaps();
    const expected = { foo: { baz: '123', lmao: true }, bar: { mmmmk: '123', lmao: false } }
    expect(myObj).to.deep.equal(expected)
  })

  afterEach(function () {
    fs.readdirSync.restore();
    fs.readFileSync.restore();
  })
})


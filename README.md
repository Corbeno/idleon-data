# idleon-data
A collection of objects that maps Legends of Idleon save data to be usable for other applications

# As a Git submodule

Refer to [this documentation](https://git-scm.com/book/en/v2/Git-Tools-Submodules) for tips on how to use this as a Git submodule
# Javascript Developers

## Installing

If you're using node.js, you are able to install this as a package to then import into your code.

Note: This project currently isn't published to npm, so you'll want to install it with the github url

Via https:
```
npm install --save https://github.com/Corbeno/idleon-data
```
Via ssh:
```
npm install --save git+https://git@github.com/Corbeno/idleon-data.git
```
## Using in your project

Simply `require` this module.

```javascript
// example.js
const myData = require('idleon-data');
```

Each `.json` file will have its own key based on the filename. e.g. `/maps/itemNames.json` will be accessable at the `itemNames` key.

## Examples

```javascript
const myData = require('idleon-data');

// Output the value for the 'Copper' item
// Should result in "Copper Ore"
console.log(myData.itemNames.Copper)

// Return all items whose value includes the word "Ore"
// {
//   Copper: 'Copper Ore',
//   Iron: 'Iron Ore',
//   Gold: 'Gold Ore',
//   Plat: 'Platinum Ore',
//   Dementia: 'Dementia Ore',
//   Void: 'Void Ore',
//   Lustre: 'Lustre Ore',
//   Starfire: 'Starfire Ore',
//   Dreadlo: 'Dreadlo Ore',
//   Godshard: 'Godshard Ore',
//   StampB5: 'Twin Ores Stamp',
//   Starlight: 'Starlight Ore'
// }
const filterPredicate = (item) => item.includes('Ore')
const filterItemValues = (items, predicate) =>
  Object.keys(items)
    .filter(itemKey => predicate(items[itemKey]))
    .reduce((filtered, itemKey) => (filtered[itemKey] = items[itemKey], filtered), {});

console.log(filterItemValues(myData.itemNames, filterPredicate))
```

## Testing

There are currently unit tests to ensure that exporting features work correctly.

```
npm test
```

# Contributing
If you would like to add to this repository, please fork this repository, make the changes, then submit a pull request. 

Each sub diretory under this one contains another README.md which lays out specific instructions for contributing (they aren't too strict don't worry!).

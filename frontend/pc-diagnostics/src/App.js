import './App.css';
import  {useState} from 'react';

const testObject = {'CPU':[{name: 'CPU_temp', t:[0,1],v:[66,55]}, {name: 'CPU_load',t:[0,1],v:['40%','44%']}], 'GPU':[{name: 'GPU_temp', t:[0,1],v:[36,37]}, {name: 'GPU_load',t:[0,1],v:['20%','21%']}]}


function App() {
  const [selectedData, setData] = useState([])

  return (
    <div className="App">
        <TopBar {...testObject}/>
    </div>
  );
}

const TopBar = (data) => {
  return (
    <div className='TopBar'>
      <div className='FilterBar'>
        {Object.entries(data).map(([component, data]) => {
          return <Dropdown text={component} id={component} items={data}/>
        })}
      </div>
    </div>
  )
}

const Dropdown = (dropdownInfo) => {
  const [isOpen, setOpen] = useState(false)

  function toggle() {
    setOpen((isOpen) => !isOpen);
  }

  let dropdownText = dropdownInfo.text;
  let dropdownID = dropdownInfo.id;
  let dropdownElements = dropdownInfo.items;
  return (
    <div className='ComponentDropdown' id={dropdownID} onClick={toggle}>
      <label className='DropdownText'>{dropdownText}</label>
      {isOpen && <DropdownItems items={dropdownElements} name={dropdownText}/>}
      
    </div>
  )
}


const DropdownItems = (itemInfo) => {
  let items = itemInfo.items;
  let name = itemInfo.name;
  return (
    <ul id={name+'_items'} className='DropdownContents'>
      {items.map((item, index) => {
        return (
          <li key={index} className='DropdownItem' onClick={(e) => e.stopPropagation()}>
            <input id={'item_'+item.name} className='DropdownItemInput' type='checkbox'/>
            <label className='DropdownItemText'>{item.name}</label>
          </li>
        )
      })}
    </ul>
  )
}



export default App;

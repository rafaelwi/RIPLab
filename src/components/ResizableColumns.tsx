import React from 'react'
import '../css/ResizableColumns.css'

type ColumnProps = {
  left: React.ReactNode,
  right: React.ReactNode
}

type ColumnsState = {
  isResizing: boolean,
  lastDownX: number,
  offset: number,
  minOffset: number
}

class ResizableColumns extends React.Component<ColumnProps, ColumnsState> {
  constructor(props: any) {
    super(props)
    this.state = {
      isResizing: false,
      lastDownX: 0,
      offset: 0,
      minOffset: 300
    }
  }

  componentDidMount() {
    const handle = document.querySelector('.colResizeHandle') as HTMLElement
    const container = document.getElementById('colResizeWrapper') as HTMLElement
    const offset = container.offsetWidth - 300;

    let self = this
    self.setState({
      offset
    })

    handle.onmousedown = (e: MouseEvent) => {
      self.setState({
        isResizing: true,
        lastDownX: e.clientX
      })
      e.preventDefault();
    }

    // Yeah I don't really get why this one is document and the other two
    // are on the handle. But it works.
    document.onmousemove = (e: MouseEvent) => {
      if (!self.state.isResizing) return;
      
      var offset = container.offsetWidth - (e.clientX - container.offsetLeft);
      const windowWidth = window.innerWidth;

      if (offset >= windowWidth - self.state.minOffset) 
        offset = windowWidth - self.state.minOffset;

      self.setState({
        offset: offset <= self.state.minOffset ? self.state.minOffset : offset
      })
    };

    handle.onmouseup = (e: MouseEvent) => {
      self.setState({
        isResizing: false
      })
    };

    handle.ondblclick = (e: MouseEvent) => {
      self.setState({
        offset: container.offsetWidth - 300
      })
    }
  }

  render() {
    if (this.props)
      return <div className={'colResizeWrapper'} id={'colResizeWrapper'}>
        <div className={'colResizeLeft'}
          style={{ right: this.state.offset }}>
          <div className={'colResizeFullCol'}>
            {this.props.left}
          </div>
        </div>
        <div className={'colResizeRight'} style={{ width: this.state.offset }}>
          <div className={'colResizeHandle'}></div>
          <div className='right-props'>
            {this.props.right}
          </div>
        </div>
      </div>

    else
      return <React.Fragment />
  }
}

export default ResizableColumns;

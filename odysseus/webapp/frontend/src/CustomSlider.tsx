import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
  ComponentProps,
} from "streamlit-component-lib";
import React, { useEffect, useState } from "react";
import { Slider } from "baseui/slider";

/**
 * Called by <CustomSlider />, renders the return value on screen.
 *
 * (props) => {code} is an arrow function, a shorter syntax for JS functions
 * equivalent to : function (props) { code; return <h1>Hello world</h1>};
 * or in Python, lambda props : return <h1>Hello world</h1>.
 *
 * When called, it will run then render on the browser the returned JSX block
 */

const CustomSlider = (props: ComponentProps) => {
  console.log(props.args);
  /**
   * Destructuring JSON objects is a good habit.
   * This will look for label, minValue and maxValue keys
   * to store them in separate variables.
   */
  const { label, minValue, maxValue } = props.args;

  // Define an internal state for your component, called "value" with an initial value of [10]
  // setValue is used to modify the state with a new Array of numbers
  const [value, setValue] = useState([10]);

    // useEffect is a specific React hook which calls its input after the component has been rendered on the browser.
  // The callback function properly sets the height of the HTML block wrapping the component.
  // By default it checks the scrollable height of the returned block after rendering and sets it as the iframe height.
    useEffect(() => Streamlit.setFrameHeight());

  // Render this React component as a stateless baseui Slider
  return (
    <>
      <h3>{label}</h3>
      <Slider
        value={value}
        onChange={({ value }) => value && setValue(value)}
        onFinalChange={({ value }) => console.log(value)}
        min = {minValue}
        max = {maxValue}
      />
    </>
  );
};

// Link the component to Streamlit JS events.
export default withStreamlitConnection(CustomSlider);

//
// interface State {
//   numClicks: number
//   isFocused: boolean
// }

/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
// class CustomSlider extends StreamlitComponentBase<State> {
//   public state = { numClicks: 0, isFocused: false }
//
//   public render = (): ReactNode => {
//     // Arguments that are passed to the plugin in Python are accessible
//     // via `this.props.args`. Here, we access the "name" arg.
//     const name = this.props.args["name"]
//
//     // Streamlit sends us a theme object via props that we can use to ensure
//     // that our component has visuals that match the active theme in a
//     // streamlit app.
//     const { theme } = this.props
//     const style: React.CSSProperties = {}
//
//     // Maintain compatibility with older versions of Streamlit that don't send
//     // a theme object.
//     if (theme) {
//       // Use the theme object to style our button border. Alternatively, the
//       // theme style is defined in CSS vars.
//       const borderStyling = `1px solid ${
//         this.state.isFocused ? theme.primaryColor : "gray"
//       }`
//       style.border = borderStyling
//       style.outline = borderStyling
//     }
//
//     // Show a button and some text.
//     // When the button is clicked, we'll increment our "numClicks" state
//     // variable, and send its new value back to Streamlit, where it'll
//     // be available to the Python program.
//     return (
//       <span>
//         Hello, {name}! &nbsp;
//         <button
//           style={style}
//           onClick={this.onClicked}
//           disabled={this.props.disabled}
//           onFocus={this._onFocus}
//           onBlur={this._onBlur}
//         >
//           Click Me!
//         </button>
//       </span>
//     )
//   }
//
//   /** Click handler for our "Click Me!" button. */
//   private onClicked = (): void => {
//     // Increment state.numClicks, and pass the new value back to
//     // Streamlit via `Streamlit.setComponentValue`.
//     this.setState(
//       prevState => ({ numClicks: prevState.numClicks + 1 }),
//       () => Streamlit.setComponentValue(this.state.numClicks)
//     )
//   }
//
//   /** Focus handler for our "Click Me!" button. */
//   private _onFocus = (): void => {
//     this.setState({ isFocused: true })
//   }
//
//   /** Blur handler for our "Click Me!" button. */
//   private _onBlur = (): void => {
//     this.setState({ isFocused: false })
//   }
// }
//
// // "withStreamlitConnection" is a wrapper function. It bootstraps the
// // connection between your component and the Streamlit app, and handles
// // passing arguments from Python -> Component.
// //
// // You don't need to edit withStreamlitConnection (but you're welcome to!).
// export default withStreamlitConnection(CustomSlider)



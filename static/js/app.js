const addInput = (event) => {
    const div = document.querySelector('#inputs');
    const text_input = getInput();
    div.appendChild(text_input);
    event.preventDefault();
    event.stopPropagation();
}

const removeInput = (event) => {
    const div = document.querySelector('#inputs');
    const text_inputs = document.querySelectorAll('.my-text');
    if(text_inputs.length > 1) {
        const text_input = text_inputs[text_inputs.length-1];
        div.removeChild(text_input);
    }
    event.preventDefault();
    event.stopPropagation();
}

const generateMindMap = (event) => {
    event.preventDefault();
    event.stopPropagation();
}

const getInput = () => {
    const text_input = document.createElement("INPUT");
    text_input.setAttribute('type', 'text');
    text_input.setAttribute('class', 'my-text');
    text_input.setAttribute('placeholder', 'Enter the URL');
    return text_input;
}
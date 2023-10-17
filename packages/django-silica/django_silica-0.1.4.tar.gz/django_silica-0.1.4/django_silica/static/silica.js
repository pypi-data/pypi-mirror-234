const ACTION_TYPE_CALL_METHOD = "call_method";
const ACTION_TYPE_SET_PROPERTY = "set_property";
const ACTION_TYPE_EVENT = "event";

let components = {};

// create class that takes component_id and name as params
// class Component {
//     // create js init
//     constructor(component_id, component_name) {
//         self.component_id = component_id
//         self.component_name = component_name
//
//         setup()
//     }
// }

// Utility function to get the closest ancestor with a specific attribute
function getCurrentComponent(elem) {
  for (; elem && elem !== document; elem = elem.parentNode) {
    if (elem.getAttribute("silica:id")) {
      return {
        el: elem,
        id: elem.getAttribute("silica:id"),
        name: elem.getAttribute("silica:name")
      };
    }
  }
  return false;
}

function updateModelValues(componentEl, data) {
  componentEl.querySelectorAll("[silica\\:model]").forEach((el) => {
    let modelName = el.getAttribute("silica:model");
    if (data[modelName]) {
      el.value = data[modelName];
    }
  });
}

function setQueryParams(data) {
  if (data["query_params"] && data["query_params"].length > 0) {
    data["query_params"].forEach((param) => {
      if (data?.[param] !== undefined) {
        setQueryParam(param, data[param]);
      }
    });
  }
}

function processJsCalls(calls = []) {
  calls.forEach((call) => {
    const fn = call.fn;
    const args = call?.args;
    window[fn](...args);
  });
}

function processEvents(events = []) {
  events.forEach((event) => {
    if (event.type === "emit") {
      // emit to all components on page
      console.log(Object.values(components));
      Object.values(components).forEach((component) => {
        const action = {
          type: ACTION_TYPE_EVENT,
          event_name: event.name,
          payload: event.payload
        };

        sendMessage(component, action);
      });
    } else if (event.type === "emit_to") {
      // emit to all components on page
      Object.values(components)
        .filter((component) => component.name === event.component_name)
        .forEach((component) => {
          const action = {
            type: ACTION_TYPE_EVENT,
            event_name: event.name,
            payload: event.payload
          };

          sendMessage(component, action);
        });
    }
  });
}

function callMethod(component, name, args) {
  const action = {
    type: ACTION_TYPE_CALL_METHOD,
    method_name: name,
    args: args
  };

  sendMessage(component, action);
}

function activateLazy(component) {
  const action = {
    type: "activate_lazy"
  };

  sendMessage(component, action);
}

function setProperty(component, name, value) {
  const action = {
    type: ACTION_TYPE_SET_PROPERTY,
    name: name,
    value: value
  };

  sendMessage(component, action);
}

function sendMessage(component, action) {
  if (!component.id || !component.name) {
    console.error(
      "No Silica component element found when processing silica:click"
    );
    return;
  }

  // Show any silica:loading elements
  showLoaders(component.el, action);

  const params = {
    name: component.name,
    id: component.id,
    page_id: pageId,
    actions: [action]
  };

  // Send the POST request using fetch
  fetch("/silica/message", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(params)
  })
    .then((response) => response.json()) // assuming server responds with json
    .then((response) => {
      if (isRedirecting(response?.js_calls)) {
        return;
      }

      updateDom(response.id, response.html);
      initComponents(); // Pick up and init any new components nested in others
      updateModelValues(component.el, response.data);
      setQueryParams(response.data);
      processJsCalls(response?.js_calls);
      processEvents(response?.event_calls);

      // if(action.type === 'activate_lazy') {
      //     component.el.removeAttribute('silica:lazy');
      //
      // }

      hideLoaders(component.el);
    })
    .catch((error) => {
      hideLoaders(component.el);
      console.error("Error:", error);
    });
}

function setQueryParam(paramName, paramValue) {
  const url = new URL(window.location);
  url.searchParams.set(paramName, paramValue);
  window.history.pushState({}, "", url);
}

// Performance TODO list
// - In an init function, cache silica:models in the component

/*
 * initiate a random page id to help idenyify all current active cache entries which will enable event emitting etc.
 * It should be characters and numbers, about 20 characters long.
 */
const pageId =
  Math.random().toString(36).substring(2, 10) +
  Math.random().toString(36).substring(2, 10);

/*
find lazy components
call the activation

 */
function initLazyComponents() {
  const lazyComponents = document.querySelectorAll("[silica\\:lazy]");

  lazyComponents.forEach((componentEl) => {
    activateLazy(getCurrentComponent(componentEl));
  });
}

function initComponents() {
  componentEls = document.querySelectorAll("[silica\\:initial-data]");

  componentEls.forEach((componentEl) => {
    const encodedData = componentEl.getAttribute("silica:initial-data");
    const decodedData = decodeURIComponent(encodedData);
    const initialState = JSON.parse(decodedData);

    if (isRedirecting(initialState.js_calls)) {
      return;
    }

    updateModelValues(componentEl, initialState);
    setQueryParams(initialState);
    processJsCalls(initialState.js_calls);
    processEvents(initialState?.event_calls);

    componentEl.removeAttribute("silica:initial-data");

    const component_id = componentEl.getAttribute("silica:id");
    const component_name = componentEl.getAttribute("silica:name");

    components[component_id] = {
      el: componentEl,
      id: component_id,
      name: component_name
    };
  });
}

function handleModelInputEvent(event) {
  const el = event.currentTarget;

  const modelName = this.getAttribute("silica:model");

  const component = getCurrentComponent(el);

  setProperty(component, modelName, this.value);
}

function handleClickEvent(event) {
  const el = event.currentTarget;
  const component = getCurrentComponent(el);

  function silicaClick(event, methodString, prevent = false) {
    if (prevent) {
      event.preventDefault();
    }

    // Check if string function call has args
    if (methodString.includes("(")) {
      const methodNameParts = methodString.split("(");
      const methodName = methodNameParts[0];

      // also remove any quotes from left or right of each arg
      const args = methodNameParts[1]
        .replace(")", "")
        .split(",")
        .map((arg) => arg.trim());
      callMethod(component, methodName, args);
    } else {
      callMethod(component, methodString);
    }
  }

  if (el.hasAttribute("silica:click")) {
    const methodString = el.getAttribute("silica:click");
    silicaClick(event, methodString);
  } else if (el.hasAttribute("silica:click.prevent")) {
    const methodString = el.getAttribute("silica:click.prevent");
    silicaClick(event, methodString);
  }
}

function setListeners() {
  const models = document.querySelectorAll("[silica\\:model]");
  models.forEach((element) => {
    element.addEventListener("input", handleModelInputEvent);
  });

  const clicksEls = document.querySelectorAll("[silica\\:click\\.prevent]");

  clicksEls.forEach((element) => {
    element.addEventListener("click", handleClickEvent);
  });
}

function removeListeners() {
  const models = document.querySelectorAll("[silica\\:model]");
  models.forEach((element) => {
    element.removeEventListener("input", handleModelInputEvent);
  });

  const clicksEls = document.querySelectorAll("[silica\\:click\\.prevent]");

  clicksEls.forEach((element) => {
    element.removeEventListener("click", handleClickEvent);
  });
}

// Create an on content loaded callback:
document.addEventListener("DOMContentLoaded", function () {
  initComponents();
  initLazyComponents();
  setListeners(); // sets things like input sync listeners
});

function updateDom(id, html) {
  const targetElement = document.querySelector('[silica\\:id="' + id + '"]');

  if (targetElement) {
    // Create a temporary div to hold the new HTML content
    let tempDiv = document.createElement("div");
    tempDiv.innerHTML = html;

    // Use morphdom to update the target element with the new content
    morphdom(targetElement, tempDiv.firstChild, {
      onBeforeElUpdated: (fromEl, toEl) => {
        // If the element being updated is an input, ignore it
        if (fromEl.tagName === "INPUT" && toEl.tagName === "INPUT") {
          return false;
        }
        if (
          fromEl.hasAttribute("silica:glued") &&
          toEl.hasAttribute("silica:glued")
        ) {
          return false;
        }
        return true; // Continue with the update for other elements
      }
    });

    removeListeners();
    setListeners();
  } else {
    console.warn(`Element with silica:id="${id}" not found.`);
  }
}

function isRedirecting(jsCalls = []) {
  // Check if we have a redirect
  const redirectFn = jsCalls.find((call) => call.fn === "_silicaRedirect");
  if (redirectFn) {
    window.location.href = redirectFn.args[0];
    return true;
  }
  return false;
}

/**
 * Get all elements that match a query, but only if they are inside the subject component
 * @param subjectComponentEl
 * @param query
 * @returns {*}
 */
function componentQuerySelectorAll(subjectComponentEl, query) {
  let nodes = [];
  const nodeList = Array.from(subjectComponentEl.querySelectorAll(query));

  for (let i = 0; i < nodeList.length; i++) {
    if (
      getCurrentComponent(nodeList[i])?.name ===
      subjectComponentEl.getAttribute("silica:name")
    ) {
      nodes.push(nodeList[i]);
    }
  }
  return nodes;
}

/**
 * Show any silica:loading elements
 * @param componentEl
 * @param action
 */
function showLoaders(componentEl, action) {
  let target_from_action = null;

  if (action?.type === ACTION_TYPE_CALL_METHOD) {
    target_from_action = action?.method_name;
  } else if (action?.type === ACTION_TYPE_SET_PROPERTY) {
    target_from_action = action?.name;
  }

  componentQuerySelectorAll(
    componentEl,
    "[silica\\:loading], [silica\\:loading\\.class]"
  ).forEach((el) => {
    if (el.hasAttribute("silica:target")) {
      const silica_target = el.getAttribute("silica:target");
      const target_without_parentheses = silica_target.split("(")[0];

      if (
        [silica_target, target_without_parentheses].includes(
          el.getAttribute("silica:target")
        )
      ) {
        el.style.display = "block";

        const classAttr = el.getAttribute("silica:loading.class");
        applyClassesToEl(el, classAttr);
      }
    } else {
      el.style.display = "block";

      const classAttr = el.getAttribute("silica:loading.class");
      applyClassesToEl(el, classAttr);
    }
  });
}

function hideLoaders(componentEl, action) {
  let target_from_action = null;

  if (action?.target === ACTION_TYPE_CALL_METHOD) {
    target_from_action = action?.method_name;
  } else if (action?.target === ACTION_TYPE_SET_PROPERTY) {
    target_from_action = action?.name;
  }

  componentQuerySelectorAll(componentEl, "[silica\\:loading]").forEach((el) => {
    if (el.hasAttribute("silica:target")) {
      const silica_target = el.getAttribute("silica:target");
      const target_without_parentheses = silica_target.split("(")[0];

      if (
        [silica_target, target_without_parentheses].includes(
          el.getAttribute("silica:target")
        )
      ) {
        el.style.display = "none";

        const classAttr = el.getAttribute("silica:loading.class");
        removeClassesFromEl(el, classAttr);
      }
    } else {
      el.style.display = "none";

      const classAttr = el.getAttribute("silica:loading.class");
      removeClassesFromEl(el, classAttr);
    }
  });
}

function applyClassesToEl(el, classes = "") {
  if (classes) {
    // Split by space to support multiple classes
    const classes_arr = classes.split(" ");
    el.classList.add(...classes_arr);
  }
}

function removeClassesFromEl(el, classes = "") {
  if (classes) {
    // Split by space to support multiple classes
    const classes_arr = classes.split(" ");
    el.classList.remove(...classes_arr);
  }
}

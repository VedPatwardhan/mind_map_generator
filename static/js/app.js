const addInput = (event) => {
  const div = document.querySelector("#inputs");
  const text_input = getInput();
  div.appendChild(text_input);
  event.preventDefault();
  event.stopPropagation();
};

const removeInput = (event) => {
  const div = document.querySelector("#inputs");
  const text_inputs = document.querySelectorAll(".my-text");
  if (text_inputs.length > 1) {
    const text_input = text_inputs[text_inputs.length - 1];
    div.removeChild(text_input);
  }
  event.preventDefault();
  event.stopPropagation();
};

const generateMindMap = (event) => {
  getMindMap(event);
};

const getMindMap = async (event) => {
  const urls = Array.from(document.querySelectorAll(".my-text")).map(
    (ele) => ele.value
  );
  await fetch(`/?url=${urls}`, {
    Accept: "application/json",
    "Content-Type": "application/json",
  })
    .then((response) => {
      return response.json();
    })
    .then((graph) => {
      graph["links"] = graph["links"].map((link) => {
        return { source: link[0], target: link[1], weight: 1, color: "black" };
      });
      graph["nodes"] = graph["nodes"].map((node) => {
        node[1]["color"] = node[1]["color"].map((color) =>
          Math.floor(color * 255)
        );
        return {
          id: node[0],
          ...node[1],
        };
      });
      drawMindMap(graph);
    });
};

const getInput = () => {
  const text_input = document.createElement("INPUT");
  text_input.setAttribute("name", "url");
  text_input.setAttribute("type", "text");
  text_input.setAttribute("class", "my-text");
  text_input.setAttribute("placeholder", "Enter the URL");
  return text_input;
};

const drawMindMap = (graph) => {
  var svg = d3.select("svg");
  var domRect = svg["_groups"][0][0].getBoundingClientRect();
  var left = Math.floor(domRect["left"]),
    top = Math.floor(domRect["top"]),
    width = Math.floor(domRect["width"]),
    height = Math.floor(domRect["height"]);
  var scrollLeft = window.pageXOffset,
    scrollTop = window.pageYOffset;

  svg.selectAll("*").remove();

  var simulation = d3
    .forceSimulation()
    .force(
      "charge",
      d3
        .forceManyBody()
        .strength(-Math.floor((1500.0 * 15.0) / graph["nodes"].length))
    )
    .force(
      "center",
      d3.forceCenter(
        left + scrollLeft + width / 2 - 50,
        top + scrollTop + height / 2 - 150
      )
    )
    .force(
      "link",
      d3.forceLink().id(function (d) {
        return d.id;
      })
    );

  var link = svg
    .append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter()
    .append("line")
    .attr("stroke-width", function(d){
      return d.weight
    })
    .attr("stroke", function(d){
      return d.color
    });

  var node = svg
    .append("g")
    .attr("class", "nodes")
    .selectAll("g")
    .data(graph.nodes)
    .enter()
    .append("g")
    .on("click", async function (d, i) {
      function getCSRFToken(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== "") {
          var cookies = document.cookie.split(";");
          for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
              cookieValue = decodeURIComponent(
                cookie.substring(name.length + 1)
              );
              break;
            }
          }
        }
        return cookieValue;
      }
      var csrftoken = getCSRFToken("csrftoken");
      await fetch(`/`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
          credentials: "include"
        },
        body: JSON.stringify({ ...graph, node_selected: i.id }),
      })
        .then((response) => {
          return response.json();
        })
        .then((graph) => {
          graph["links"] = graph["links"].map((link) => {
            if(link[0] === i.id || link[1] === i.id)
              return { source: link[0], target: link[1], weight: 3, color: `rgb(${i.color[0]},${i.color[1]},${i.color[2]})` };
            return { source: link[0], target: link[1], weight: 1, color: "black" };
          });
          graph["nodes"] = graph["nodes"].map((node) => {
            node[1]["color"] = node[1]["color"].map((color) =>
              Math.floor(color * 255)
            );
            return {
              id: node[0],
              ...node[1],
            };
          });
          drawMindMap(graph);
        });
    });

  var circles = node
    .append("circle")
    .attr("r", 5)
    .attr("fill", function (d) {
      return `rgb(${d.color[0]},${d.color[1]},${d.color[2]})`;
    });

  var lables = node
    .append("text")
    .text(function (d) {
      return d.id;
    })
    .attr("x", 6)
    .attr("y", 3)
    .style("font-weight", "bold")

  node.append("title").text(function (d) {
    return d.id;
  });

  simulation.nodes(graph.nodes).on("tick", ticked);

  simulation.force("link").links(graph.links);

  function ticked() {
    link
      .attr("x1", function (d) {
        return d.source.x;
      })
      .attr("y1", function (d) {
        return d.source.y;
      })
      .attr("x2", function (d) {
        return d.target.x;
      })
      .attr("y2", function (d) {
        return d.target.y;
      });

    node.attr("transform", function (d) {
      return "translate(" + d.x + "," + d.y + ")";
    });
  }
};

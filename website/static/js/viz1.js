var STATIC = window.location.protocol + "//" + window.location.host + "/static/js/";

// packages.js
console.log( "Loading packages.js" );
(function() {
    packages = {

        // Lazily construct the package hierarchy from class names.
        root: function(classes) {
            var map = {};

            function find(name, data) {
                var node = map[name], i;
                if (!node) {
                    node = map[name] = data || {name: name, children: []};
                    if (name.length) {
                        node.parent = find(name.substring(0, i = name.lastIndexOf(".")));
                        node.parent.children.push(node);
                        node.key = name.substring(i + 1);
                    }
                }
                return node;
            }

            classes.forEach(function(d) {
                find(d.name, d);
            });

            return map[""];
        },

        // Return a list of imports for the given array of nodes.
        imports: function(nodes) {
            var map = {}, imports = [];

            // Compute a map from name to node.
            nodes.forEach(function(d) {
                map[d.name] = d;
            });

            // For each import, construct a link from the source to target node.
            nodes.forEach(function(d) {
                if (d.imports) {
                    d.imports.forEach(function(i) {
                        imports.push({source: map[d.name], target: map[i]});
                    });
                }
            });

            return imports;
        }

    };
})();
// end packages.js

console.log( "Preparing visualization." );

var radius = 1200 / 2, xpad = 20, ypad = 10;
var splines = [];
var m0, m1;

var cluster = d3.layout.cluster()
    .size([360, radius - 120])
    .sort(function(a, b) { return d3.ascending(a.key, b.key); })
    .value(function(d) { return d.size; });

var bundle = d3.layout.bundle();

var line = d3.svg.line.radial()
    .interpolate("bundle")
    .tension(0.85)
    .radius(function(d) { return d.y; })
    .angle(function(d) { return d.x / 180 * Math.PI; });

var vis = d3.select("#chart").append("svg")
    .attr("width", radius * 2)
    .attr("height", radius * 2)
    .append("g")
    .attr("transform", "translate(" + (radius+xpad) + "," + (radius+ypad) + ")");

d3.json((STATIC+"viz/mp.json"), function(classes) {
    var nodes = cluster.nodes(packages.root(classes)),
    links = packages.imports(nodes);

    vis.selectAll("path.link")
        .data(splines = bundle(links))
        .enter().append("path")
        .attr("class", "link")
        .attr("d", function(d, i) { return line(splines[i]); });

    vis.selectAll("g.node")
        .data(nodes.filter(function(n) { return !n.children; }))
        .enter().append("g")
        .attr("class", "node")
        .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; })
        .append("text")
        .attr("dx", function(d) { return d.x < 180 ? 8 : -8; })
        .attr("dy", ".31em")
        .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
        .attr("transform", function(d) { return d.x < 180 ? null : "rotate(180)"; })
        .text(function(d) { return d.key; });
});

function mouse(e) {
    return [e.pageX - radius, e.pageY - radius];
}

function diff(a, b) {
    return (b[0] - a[0]) + (b[1] - a[1]);
}

function map(difference) {
    var min = 0, max = 1, mid = 0.5;
    result = mid + (2 * difference / radius);
    if (result > max) {
        return max;
    } else if (result < min) {
        return min;
    } else {
        return result;
    }
}

function mouseDown() {
    m0 = mouse(d3.event);
    d3.event.preventDefault();
}

function mouseMove() {
    if (m0) {
        m1 = mouse(d3.event);
        var val = map(diff(m0, m1));
        vis.selectAll("path.link")
            .data(splines)
            .attr("d", line.tension(val));
    }
}

function mouseUp() {
    m0 = null;
}

d3.select(window)
    .on("mousedown", mouseDown)
    .on("mousemove", mouseMove)
    .on("mouseup", mouseUp);

import * as d3 from 'd3'
import { scaleLinear } from 'd3-scale'
import { curveCardinal, lineRadial, symbol, symbolCircle, symbolDiamond } from 'd3-shape'
import { zip } from 'd3-array'

const width = 400
const height = 800
const marginTop = 20
const marginRight = 30
const marginBottom = 30
const marginLeft = 40

const response = await fetch('http://jieter.github.io/orc-data/site/data/NOR/NOR3325.json')
const dataset = (await response.json()).vpp
const colors = ['blue', 'orange', 'green', 'red', 'purple', 'teal', 'pink']

const svg = d3
    .select('#polar')
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .attr('style', 'font: 10px sans-serif; overflow: visible;')
    .append('g')
    .attr('transform', `translate(30, ${height / 2.2})`)

const radius = function () {
    return Math.min(height / 1.8 - 20, width) - 15
}
const r = scaleLinear().domain([0, 10]).range([0, radius()])

const speedScale = svg
    .append('g')
    .selectAll('g')
    .data([2, 4, 6, 8, 10])
    .enter()
    .append('g')
    .attr('class', (d) => `r axis sog-${d}`)
    .attr('style', 'fill: none; stroke: #777; stroke-dasharray: 1, 4;')

speedScale.append('circle').attr('r', r)
speedScale
    .append('text')
    .attr('y', (speed) => -r(speed) - 2)
    .attr('transform', 'rotate(10)')
    .style('text-anchor', 'middle')
    .text((speed) => (speed <= 10 ? `${speed}kts` : '')) // show labels up to 10kts
    .attr('style', 'fill: black; stroke: none; stroke-dasharray: none;')

// True wind directions
const graph = svg
    .append('g')
    .attr('class', 'a axis')
    .selectAll('g')
    .data([0, 30, 45, 52, 60, 75, 90, 110, 120, 135, 150, 165, 180])
    .enter()
    .append('g')
    .attr('transform', (bearing) => `rotate(${bearing - 90})`)

graph.append('line').attr('x1', r(1)).attr('x2', radius()).attr('style', 'stroke: #777; stroke-dasharray: 1, 4;')

const xaxis = function (selection) {
    selection
        .attr('x', radius() + 6)
        .attr('dy', '.35em')
        .attr('transform', (d) => (d > 90 ? `rotate(0 ${radius() + 8}, 0)` : null))
        .text((bearing) => `${bearing}°`)
}

graph.append('text').attr('class', 'xlabel').call(xaxis)

var line = lineRadial()
    .radius((d) => r(d[1]))
    .angle((d) => d[0])
    .curve(curveCardinal)

const DEG2RAD = 0.0174532925
export function vmg2sog(beat_angle, vmg) {
    return vmg / Math.cos(beat_angle * DEG2RAD)
}
const deg2rad = (degrees, vmg) => [degrees * DEG2RAD, vmg2sog(degrees, vmg)]

function seriesFromVpp(vpp) {
    const vpp_angles = vpp.angles.map((d) => d * DEG2RAD)
    let run_data: number[][] = []

    const vpp_data = vpp.speeds.map(function (windspeed, i) {
        var series = zip(
            vpp_angles,
            vpp.angles.map((angle) => vpp[angle][i]),
        )
        // filter points with zero SOG
        // series = series.filter((a) => a[1] > 0)

        if (vpp.beat_angle) {
            series.unshift(deg2rad(vpp.beat_angle[i], vpp.beat_vmg[i]))
        }
        if (vpp.run_angle) {
            var run = deg2rad(vpp.run_angle[i], -vpp.run_vmg[i])
            series.push(run)
            run_data.push(run)
        }

        return series.sort((a, b) => a[0] - b[0])
    })
    return { vpp_data, run_data }
}

var scatter = function (shape?, size?) {
    return function (s) {
        s.attr('transform', (d) => `translate(${r(d[1]) * Math.sin(d[0])}, ${r(d[1]) * -Math.cos(d[0])})`)
        s.attr('d', symbol(shape || symbolDiamond, size || 32))
        s.attr('style', (d, i) => `fill: none; stroke: ${colors[i]};`)
    }
}

var scatterText = function (shape?, size?) {
    return function (s) {
        s.attr('transform', (d) => `translate(${-30}, ${r(d[1]) * -Math.cos(d[0]) + 4})`)
            .text((d, i) => `${dataset.speeds[i]}kts`)
            .attr('style', (d, i) => `fill: ${colors[i]};`)
    }
}
const { vpp_data, run_data } = seriesFromVpp(dataset)

var tws_series = function (cssClass) {
    return (selection) => selection.attr('class', (d, i) => `${cssClass} tws-${dataset.speeds[i]}`)
}

var run_points = svg.selectAll('.vmg-run').data(run_data)
run_points.exit().remove()
run_points.enter().append('path').call(tws_series('vmg-run')).merge(run_points).call(scatter())
// .attr('style', 'fill: none; stroke: black;')
run_points.enter().append('text').call(tws_series('vmg-run')).merge(run_points).call(scatterText())

var lines = svg.selectAll('.line').data(vpp_data)
lines.exit().remove()
lines
    .enter()
    .append('path')
    .call(tws_series('line'))
    .merge(lines)
    .attr('d', line)
    .attr('style', (d, i) => `fill: none; stroke: ${colors[i]};`)

// const twsScale = svg
//     .append('g')
//     .selectAll('g')
//     .data(dataset.speeds)
//     .enter()
//     .append('g')
//     // .attr('class', (d) => `r axis sog-${d}`)
//     .attr('style', 'fill: none; stroke: #777; stroke-dasharray: 1, 4;')

// twsScale.append('circle').attr('r', r)
// lines
//     .append('text')
//     .attr('y', (speed) => -r(speed) - 2)
//     // .attr('transform', 'rotate(10)')
//     .style('text-anchor', 'middle')
//     .text((speed) => (speed <= 10 ? `${speed}kts` : '')) // show labels up to 10kts
//     .attr('style', 'fill: black; stroke: none; stroke-dasharray: none;')

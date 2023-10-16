<script>
  import { bisect, extent } from "d3-array";
  import { scaleLinear } from "d3-scale";
  import { line, curveBasis, area } from "d3-shape";
  import { data } from "./data";
  import { select } from "d3-selection";

  let outerHeight;
  let outerWidth;

  let m = { x: 0, y: 0 };

  function handleMousemove(event) {
    select("#annotation-tooltip").style("opacity", 1);
    m.x = event.clientX - event.currentTarget.getBoundingClientRect().left;
    m.y = event.clientY - event.currentTarget.getBoundingClientRect().top;
    if (m.x < margin.left) {
      m.x = margin.left;
      //   select("#annotation-tooltip").style("opacity", 0);
    }
    if (m.x > width - margin.right) {
      m.x = width - margin.right;
      //   select("#annotation-tooltip").style("opacity", 0);
    }
    // if (m.y > height - margin.right) {
    //   m.y = width - margin.right;
    //   select("#annotation-tooltip").style("opacity", 0);
    // }
    // if (m.y > height - margin.right) {
    //   m.y = width - margin.right;
    //   select("#annotation-tooltip").style("opacity", 0);
    // }
  }

  function handleMouseout(event) {
    console.log("out");
    select("#annotation-tooltip").style("opacity", 0);
  }

  let margin = {
    top: 10,
    bottom: 15,
    left: 35,
    right: 0,
  };

  $: width = outerWidth - margin.left - margin.right;
  $: height = outerHeight - margin.top - margin.bottom;

  // scales
  $: xScale = scaleLinear()
    .domain(extent(data.map((d) => d.epoch)))
    .range([margin.left, width - margin.right]);

  $: yScale = scaleLinear()
    .domain(extent(data.map((d) => d.error)))
    .range([height - margin.bottom, margin.top]);

  // the path generator
  $: pathLine = line()
    .x((d) => xScale(d.epoch))
    .y((d) => yScale(d.error));
  // .curve(curveBasis);

  $: pathArea = area()
    .x((d) => xScale(d.epoch))
    .y0(height - margin.bottom)
    .y1((d) => yScale(d.error));
  // .curve(curveBasis);
</script>

<div
  class="chart-holder"
  bind:offsetWidth={outerWidth}
  bind:offsetHeight={outerHeight}
>
  <svg
    width={outerWidth}
    height={outerHeight}
    on:touchmove={handleMousemove}
    on:mousemove={handleMousemove}
    on:mouseleave={handleMouseout}
    on:touchend={handleMouseout}
  >
    <defs>
      <linearGradient id="area-gradient" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" style="stop-color: #FF5470; stop-opacity: 1" />
        <stop offset="100%" style="stop-color: white; stop-opacity: .2" />
      </linearGradient>
    </defs>

    <path class="area-path" d={pathArea(data)} fill="url(#area-gradient)" />
    <path class="outer-path" d={pathLine(data)} />
    <path class="inner-path" d={pathLine(data)} />

    <line
      class="axis-line"
      x1={margin.left}
      x2={width - margin.right}
      y1={height - margin.bottom}
      y2={height - margin.bottom}
    />
    <line
      class="axis-line"
      x1={margin.left}
      x2={margin.left}
      y1={margin.top}
      y2={height - margin.bottom}
    />
    <!-- x-ticks -->
    {#each xScale.ticks() as tick}
      <g transform={`translate(${xScale(tick) + 0} ${height - margin.bottom})`}>
        <line
          class="axis-tick"
          x1="0"
          x2="0"
          y1={0}
          y2={-height + margin.bottom + margin.top}
          stroke="black"
          stroke-dasharray="4"
        />
        <text class="axis-text" y="15" text-anchor="middle">{tick}</text>
      </g>
    {/each}
    <!-- y-ticks -->
    {#each yScale.ticks() as tick}
      <g transform={`translate(${margin.left} ${yScale(tick) + 0})`}>
        <line
          class="axis-tick"
          x1={0}
          x2={width - margin.right - margin.left}
          y1="0"
          y2="0"
          stroke="black"
          stroke-dasharray="4"
        />
        <text
          class="axis-text"
          x="-5"
          y="0"
          text-anchor="end"
          dominant-baseline="middle">{tick}</text
        >
      </g>
    {/each}

    <!-- axis labels -->
    <text
      class="chart-title"
      y={margin.top / 2}
      x={(width + margin.left) / 2}
      text-anchor="middle"
    />
    <text
      class="axis-label"
      y={height + margin.bottom + 2}
      x={(width + margin.left) / 2}
      text-anchor="middle"
    />
    <text
      class="axis-label"
      y={margin.left / 2}
      x={-(height / 2)}
      text-anchor="middle"
      transform="rotate(-90)"
    />

    <!-- tooltip -->
    <line
      id="annotation-tooltip"
      x1={m.x}
      y1={height - margin.bottom}
      x2={m.x}
      y2={margin.top}
      stroke-width="4"
      stroke="black"
    />
    <circle
      id="annotation-tooltip-circle"
      r="10"
      cx={m.x}
      cy={m.y}
      fill="red"
    />
  </svg>
</div>

<style>
  .chart-holder {
    height: 100%;
    width: 100%;
  }
  .axis-line {
    stroke-width: 3;
    stroke: black;
    fill: none;
  }
  .axis-tick {
    stroke-width: 1;
    stroke: black;
    fill: none;
    opacity: 0.05;
  }
  .axis-text {
    font-family: Arial;
    font-size: 12px;
  }

  .inner-path {
    stroke: #ff5470;
    stroke-width: 4;
    fill: none;
    stroke-linecap: round;
  }
  .outer-path {
    stroke: white;
    stroke-width: 5;
    opacity: 1;
    fill: none;
    stroke-linecap: round;
  }

  .area-path {
    opacity: 0.76; /* adjust for your preferred opacity */
  }
</style>

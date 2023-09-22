const elem_stw = document.querySelector('#stw')!
const elem_sog = document.querySelector('#sog')!
const elem_tws = document.querySelector('#tws')!
const elem_aws = document.querySelector('#aws')!
const elem_twa = document.querySelector('#twa')!
const elem_awa = document.querySelector('#awa')!

const ws = new WebSocket('ws://localhost:8001')
ws.onopen = () => {
    console.log('open')
}

ws.onclose = () => {
    console.log('close')
}
ws.onmessage = ({ data }) => {
    console.log(data)

    const { stw, sog, tws, aws, twa, awa } = JSON.parse(data)
    elem_stw.innerHTML = `${stw.toFixed(2)}`
    elem_sog.innerHTML = `${sog.toFixed(2)}`
    elem_tws.innerHTML = `${tws.toFixed(2)}`
    elem_aws.innerHTML = `${aws.toFixed(2)}`
    elem_twa.innerHTML = `${Math.round(twa)}°`
    elem_awa.innerHTML = `${Math.round(awa)}°`
}

const elem_tws = document.querySelector('#tws')!
const elem_awa = document.querySelector('#awa')!
const elem_stw = document.querySelector('#stw')!

const ws = new WebSocket('ws://localhost:8001')
ws.onopen = () => {
    console.log('open')
}

ws.onclose = () => {
    console.log('close')
}
ws.onmessage = ({ data }) => {
    console.log(data)

    const { tws, awa, stw } = JSON.parse(data)
    elem_tws.innerHTML = tws
    elem_awa.innerHTML = awa
    elem_stw.innerHTML = stw
}

const tbody = document.querySelector('#polar-table tbody')!
const thead = document.querySelector('#polar-table thead')!

export function populate_table(data, colors) {
    const tr = document.createElement('tr')
    const td = document.createElement('td')
    td.innerHTML = 'TWA'
    tr.append(td)
    for (const tws of data.speeds) {
        const th = document.createElement('th')
        th.innerHTML = `${tws}`
        th.classList.add(`tws-${tws}`)
        tr.append(th)
    }
    thead.append(tr)

    for (const twa of data.angles) {
        const tr = document.createElement('tr')
        const td = document.createElement('td')
        td.innerHTML = twa
        tr.append(td)
        for (const [i, speed] of data[twa].entries()) {
            const td = document.createElement('td')
            td.innerHTML = speed
            td.classList.add(`tws-${data.speeds[i]}`)
            tr.append(td)
        }
        tbody.append(tr)
    }
}

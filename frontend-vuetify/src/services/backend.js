import axios from 'axios';
import querystring from 'querystring';

const Backend = {
    fetch({ baseUrl, params, page, itemsPerPage, sortBy, groupBy, column_filter, search }) {
        return new Promise(resolve => {
            setTimeout(async () => {

                console.log({
                    in: "BACKEND",
                    baseUrl: baseUrl,
                    params: params,
                    page: page,
                    itemsPerPage: itemsPerPage,
                    groupBy: groupBy,
                    sortBy: sortBy,
                    column_filter: column_filter,
                    q: search
                })

                params.page = page
                params.limit = itemsPerPage
                if (column_filter) {
                    params.column_filter = column_filter
                }
                if (search) {
                    params.q = search
                }

                if (sortBy.length) {
                    params.order_by = sortBy[0].key
                    params.sort_dir = sortBy[0].order
                }

                const query = querystring.stringify(params)
                const url = `${baseUrl}?${query}`
                const response = await axios.get(url)
                const data = response.data

                resolve({ items: data.data, total: data._meta.count })
            }, 500)
        })
    },
}

export default Backend
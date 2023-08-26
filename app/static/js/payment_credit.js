const theadHistorialPayment = document.querySelector('#theadHistorialPayment');
const tbodyHistorialPayment = document.querySelector('#tbodyHistorialPayment');
const creditWithoutPayment = document.querySelector('#creditWithoutPayment');
const modalCompanyMessage = document.querySelector('#modalCompanyMessage');

if (modalCompanyMessage) {
    const quotingModal = new bootstrap.Modal(document.getElementById('modalCompanyMessage'));
    quotingModal.show();
}

const getPaymentCredit = (server, creditId) => {
    creditWithoutPayment.classList.add('d-none');
    theadHistorialPayment.innerHTML = '';
    tbodyHistorialPayment.innerHTML = '';
    if (creditId != '') ajaxRequest(server, creditId);    
};

const createTdTable = (amount, createdAt) => {
    let data = new Date(createdAt);
    createdAtFormat = data.toLocaleString();

    const tr = document.createElement('tr');

    const td1 = document.createElement('td');
    td1.innerHTML = amount;
    
    const td2 = document.createElement('td');
    td2.innerHTML = createdAtFormat;
   
    tr.appendChild(td1); 
    tr.appendChild(td2); 
    tbodyHistorialPayment.appendChild(tr); 
}

const createThTable = () => {
    const tr = document.createElement('tr');

    const th1 = document.createElement('th');
    th1.innerHTML = 'Valor';
    
    const th2 = document.createElement('th');
    th2.innerHTML = 'Fecha';
   
    tr.appendChild(th1); 
    tr.appendChild(th2);
    theadHistorialPayment.appendChild(tr); 
}

ajaxRequest = (server, creditId) => { 
    fetch(`${server}/payment_credit_ajax_card/${creditId}/Sales0349$e443/`, {
        method: 'get',
        headers: { 
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.length > 0) {
            createThTable();
            data.forEach(element => {
                createTdTable(element.amount, element.created_at);
            });
        } else {
            alert('entra');
            creditWithoutPayment.classList.remove('d-none');
        }
    })
    .catch((error) => {     
        console.group(error)
    });
}

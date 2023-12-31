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

const createTdTable = (amount, concept, creditBalance, createdAt) => {
    let data = new Date(createdAt);
    createdAtFormat = data.toLocaleString();

    const tr = document.createElement('tr');

    const td1 = document.createElement('td');
    td1.innerHTML = amount;

    const td2 = document.createElement('td');
    td2.innerHTML = concept;

    const td3 = document.createElement('td');
    td3.innerHTML = creditBalance
    
    const td4 = document.createElement('td');
    td4.innerHTML = createdAtFormat;
   
    tr.appendChild(td1); 
    tr.appendChild(td2); 
    tr.appendChild(td3); 
    tr.appendChild(td4); 
    tbodyHistorialPayment.appendChild(tr); 
}

const createThTable = () => {
    const tr = document.createElement('tr');

    const th1 = document.createElement('th');
    th1.innerHTML = 'Valor';

    const th2 = document.createElement('th');
    th2.innerHTML = 'Concepto';
    
    const th3 = document.createElement('th');
    th3.innerHTML = 'Saldo del Crédito';

    const th4 = document.createElement('th');
    th4.innerHTML = 'Fecha';
   
    tr.appendChild(th1); 
    tr.appendChild(th2);
    tr.appendChild(th3);
    tr.appendChild(th4);
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
            data.forEach((element) => {
                let concept = 'ABONO';
                if (element.concept == 'DESEMBOLSO') {
                    concept = 'VENTA';
                    element.amount = '';
                }
                createTdTable(
                    element.amount, 
                    concept, 
                    element.credit_balance, 
                    element.created_at,
                );
            });
        } else {
            creditWithoutPayment.classList.remove('d-none');
        }
    })
    .catch((error) => {     
        console.group(error)
    });
}

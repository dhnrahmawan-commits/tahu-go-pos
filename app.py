import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="POS Tahu Go", layout="centered", page_icon="🍢")
st.title("🍢 POS Kasir Tahu Go")

# Database sementara dalam sesi
if "transaksi" not in st.session_state:
    st.session_state.transaksi = []

# Daftar Harga
MENU_OFFLINE = {
    "Tahu Go isi 5 (Rp 10.000)": (10000, 5),
    "Tahu Go isi 10 (Rp 20.000)": (20000, 10),
    "Tahu Go isi 15 (Rp 30.000)": (30000, 15),
    "Tahu Go isi 20 (Rp 40.000)": (40000, 20),
    "Taburi BBQ (Rp 4.500)": (4500, 0),
    "Taburi Gas Pedas (Rp 4.500)": (4500, 0),
    "Extra Sambal (Rp 3.500)": (3500, 0),
}

MENU_ONLINE = {
    "Tahu Go isi 5 (Rp 12.500)": (12500, 5),
    "Tahu Go isi 10 (Rp 24.900)": (24900, 10),
    "Tahu Go isi 15 (Rp 37.500)": (37500, 15),
    "Tahu Go isi 20 (Rp 49.800)": (49800, 20),
    "Taburi BBQ (Rp 4.500)": (4500, 0),
    "Taburi Gas Pedas (Rp 4.500)": (4500, 0),
    "Extra Sambal (Rp 3.500)": (3500, 0),
}

tab1, tab2 = st.tabs(["📝 Input Transaksi", "📊 Dashboard & Laporan"])

with tab1:
    metode = st.selectbox("Pilih Metode Pembayaran", ["CASH", "QRIS", "GOFOOD", "SHOPEEFOOD", "GRABFOOD"])
    menu_dict = MENU_OFFLINE if metode in ["CASH", "QRIS"] else MENU_ONLINE
    
    item_pilihan = st.selectbox("Pilih Menu", list(menu_dict.keys()))
    jumlah = st.number_input("Jumlah Porsi", min_value=1, value=1, step=1)
    
    if st.button("Simpan Transaksi", type="primary"):
        harga_satuan, pcs_satuan = menu_dict[item_pilihan]
        total_harga = harga_satuan * jumlah
        total_pcs = pcs_satuan * jumlah
        gaji = total_pcs * 150
        tgl = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        st.session_state.transaksi.append({
            "Tanggal": tgl,
            "Metode": metode,
            "Total_Harga": total_harga,
            "Total_Pcs": total_pcs,
            "Gaji": gaji
        })
        st.success(f"Berhasil disimpan! Total: Rp {total_harga:,} | Gaji: Rp {gaji:,}")

with tab2:
    if len(st.session_state.transaksi) > 0:
        df = pd.DataFrame(st.session_state.transaksi)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Omset", f"Rp {df['Total_Harga'].sum():,}")
        col2.metric("Tahu Terjual", f"{df['Total_Pcs'].sum()} pcs")
        col3.metric("Gaji Karyawan", f"Rp {df['Gaji'].sum():,}")
        
        st.subheader("Omset per Channel Pembayaran")
        st.dataframe(df.groupby("Metode")[["Total_Harga", "Total_Pcs", "Gaji"]].sum(), use_container_width=True)
        
        st.subheader("Riwayat Transaksi")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Belum ada data transaksi tersimpan.")

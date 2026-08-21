import styles from './WelcomePage.module.css';

export default function WelcomePage({ onLogout }) {
  return (
    <div className={styles.wrapper}>
      <header className={styles.header}>
        <span className={styles.logoMark}>PS</span>
        <button className={styles.logoutBtn} onClick={onLogout}>
          Cerrar sesión
        </button>
      </header>

      <main className={styles.main}>
        <h1 className={styles.heading}>Bienvenido</h1>
        <p className={styles.body}>
          Has iniciado sesión correctamente. Tu sesión está protegida con un token JWT.
        </p>
      </main>
    </div>
  );
}

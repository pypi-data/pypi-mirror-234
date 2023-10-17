!!$*****************************************************************************
!!$*****************************************************************************
!!$*****************************************************************************
!!$ fort_spec.f90: utility functions to calculate cloud opacities, optical
!!$ depths, spectra, and spectral contribution functions for the petitRADTRANS
!!$ radiative transfer package.
!!$
!!$ Copyright 2016-2018, Paul Molliere
!!$ Maintained by Paul Molliere, molliere@strw.leidenunivl.nl
!!$ Status: under development
!!$*****************************************************************************
!!$*****************************************************************************
!!$*****************************************************************************

!!$ Natural constants block

module constants_block
  implicit none
  DOUBLE PRECISION,parameter      :: AU = 1.49597871d13, R_sun = 6.955d10, R_jup=6.9911d9
  DOUBLE PRECISION,parameter      :: pi = 3.14159265359d0, sig=5.670372622593201d-5, c_l=2.99792458d10
  DOUBLE PRECISION,parameter      :: G = 6.674d-8, M_jup = 1.89813d30, deg = Pi/1.8d2
  DOUBLE PRECISION,parameter      :: kB=1.3806488d-16, hplanck=6.62606957d-27, amu = 1.66053892d-24
  DOUBLE PRECISION,parameter      :: sneep_ubachs_n = 25.47d18, L0 = 2.68676d19
end module constants_block

!!$ #########################################################################
!!$ #########################################################################
!!$ #########################################################################
!!$ #########################################################################
!!$ Subroutine to calculate the Phasecurve

subroutine feautrier_rad_trans_phase_curve(border_freqs, &
     tau_approx_scat, &
     temp, &
     mu, &
     w_gauss_mu, &
     w_gauss_ck, &
     photon_destruct_in, &
     surf_refl, &
     surf_emi, &
     I_star_0, &
     geom, &
     mu_star, &
     do_scat, &
     flux, &
     I_GCM, &
     freq_len_p_1, &
     struc_len, &
     N_mu, &
     N_g)

  use constants_block
  implicit none

  ! I/O
  INTEGER, INTENT(IN)             :: freq_len_p_1, struc_len, N_mu, N_g
  DOUBLE PRECISION, INTENT(IN)    :: mu_star
  DOUBLE PRECISION, INTENT(IN)    :: surf_refl(freq_len_p_1-1),surf_emi(freq_len_p_1-1) !ELALEI
  DOUBLE PRECISION, INTENT(IN)    :: I_star_0(freq_len_p_1-1) !ELALEI
  DOUBLE PRECISION, INTENT(IN)    :: border_freqs(freq_len_p_1)
  DOUBLE PRECISION, INTENT(IN)    :: tau_approx_scat(N_g,freq_len_p_1-1,struc_len)
  DOUBLE PRECISION, INTENT(IN)    :: temp(struc_len)
  DOUBLE PRECISION, INTENT(IN)    :: mu(N_mu)
  DOUBLE PRECISION, INTENT(IN)    :: w_gauss_mu(N_mu), w_gauss_ck(N_g)
  DOUBLE PRECISION, INTENT(IN)    :: photon_destruct_in(N_g,freq_len_p_1-1,struc_len)
  LOGICAL, INTENT(IN)             :: do_scat
  DOUBLE PRECISION, INTENT(OUT)   :: flux(freq_len_p_1-1)
  CHARACTER*20, intent(in)        :: geom
  DOUBLE PRECISION, INTENT(OUT)   :: I_GCM(N_mu,freq_len_p_1-1)

  ! Internal
  INTEGER                         :: j,i,k,l, i_mu
  DOUBLE PRECISION                :: I_J(struc_len,N_mu), I_H(struc_len,N_mu)
  DOUBLE PRECISION                :: source(N_g,freq_len_p_1-1,struc_len), &
       J_planet_scat(N_g,freq_len_p_1-1,struc_len), &
       photon_destruct(N_g,freq_len_p_1-1,struc_len), &
       source_planet_scat_n(N_g,freq_len_p_1-1,struc_len), &
       source_planet_scat_n1(N_g,freq_len_p_1-1,struc_len), &
       source_planet_scat_n2(N_g,freq_len_p_1-1,struc_len), &
       source_planet_scat_n3(N_g,freq_len_p_1-1,struc_len)
   DOUBLE PRECISION                :: J_star_ini(N_g,freq_len_p_1-1,struc_len)
   DOUBLE PRECISION                :: I_star_calc(N_g,N_mu,struc_len,freq_len_p_1-1)

  ! tridag variables
  DOUBLE PRECISION                :: a(struc_len),b(struc_len),c(struc_len),r(struc_len), &
       planck(struc_len)
  DOUBLE PRECISION                :: f1,f2,f3, deriv1, deriv2, I_plus, I_minus

  ! quantities for P-T structure iteration
  DOUBLE PRECISION                :: J_bol(struc_len)
  DOUBLE PRECISION                :: J_bol_a(struc_len)
  DOUBLE PRECISION                :: J_bol_g(struc_len)

  ! ALI
  DOUBLE PRECISION                :: lambda_loc(N_g,freq_len_p_1-1,struc_len)

  ! control
  DOUBLE PRECISION                :: inv_del_tau_min
  INTEGER                         :: iter_scat, i_iter_scat
  DOUBLE PRECISION                :: conv_val
  DOUBLE PRECISION                :: I_GCM_OLD(N_mu,freq_len_p_1-1)

  ! GCM spec calc
  LOGICAL                         :: GCM_read

  ! PAUL NEW
  ! Variables for surface scattering
  DOUBLE PRECISION                :: I_plus_surface(N_mu, N_g, freq_len_p_1-1)

    ! Source convergence



  I_plus_surface = 0d0
  I_minus = 0d0
  ! END PAUL NEW

  GCM_read = .TRUE.
  iter_scat = 1000
  if (.not. do_scat) then
      iter_scat = 1
  end if
  source = 0d0
  I_GCM = 0d0
  I_GCM_OLD = 0d0


  source_planet_scat_n = 0d0
  source_planet_scat_n1 = 0d0
  source_planet_scat_n2 = 0d0
  source_planet_scat_n3 = 0d0

  photon_destruct = photon_destruct_in

  ! DO THE STELLAR ATTENUATION CALCULATION

  J_star_ini = 0d0


  do i = 1, freq_len_p_1-1
    ! Irradiation treatment
    ! Dayside ave: multiply flux by 1/2.
    ! Planet ave: multiply flux by 1/4

    do i_mu = 1, N_mu
      if (trim(adjustl(geom)) .EQ. 'dayside_ave') then
           I_star_calc(:,i_mu,:,i) = 0.5* abs(I_star_0(i))*exp(-tau_approx_scat(:,i,:)/mu(i_mu))
           J_star_ini(:,i,:) = J_star_ini(:,i,:)+0.5d0*I_star_calc(:,i_mu,:,i)*w_gauss_mu(i_mu)
      else if (trim(adjustl(geom)) .EQ. 'planetary_ave') then
           I_star_calc(:,i_mu,:,i) = 0.25* abs(I_star_0(i))*exp(-tau_approx_scat(:,i,:)/mu(i_mu))
           J_star_ini(:,i,:) = J_star_ini(:,i,:)+0.5d0*I_star_calc(:,i_mu,:,i)*w_gauss_mu(i_mu)
      else if (trim(adjustl(geom)) .EQ. 'non-isotropic') then
           J_star_ini(:,i,:) = abs(I_star_0(i)/4.*exp(-tau_approx_scat(:,i,:)/mu_star))
      else
          write(*,*) 'Invalid geometry'
     end if
   end do
  end do

  main_loop: do i_iter_scat = 1, iter_scat

    !write(*,*) 'i_iter_scat', i_iter_scat

    lambda_loc = 0d0

    J_planet_scat = 0d0

    inv_del_tau_min = 1d10
    J_bol(1) = 0d0
    I_GCM_OLD = I_GCM
    I_GCM = 0d0
    do i = 1, freq_len_p_1-1

       flux(i) = 0d0
       J_bol_a = 0d0

       r = 0

       call planck_f_lr(struc_len,temp(1:struc_len),border_freqs(i),border_freqs(i+1),r)
       planck = r

       do l = 1, N_g

          if (i_iter_scat .EQ. 1) then
              if (do_scat) then
                source(l,i,:) = photon_destruct(l,i,:)*r +  (1d0-photon_destruct(l,i,:))*J_star_ini(l,i,:)
              else
                source(l,i,:) = r
              end if
          else
             r = source(l,i,:)

          end if


          do j = 1, N_mu



             ! Own boundary treatment
             f1 = mu(j)/(tau_approx_scat(l,i,1+1)-tau_approx_scat(l,i,1))

             ! own test against instability
             if (f1 > inv_del_tau_min) then
                f1 = inv_del_tau_min
             end if
             if (f1 .NE. f1) then
                f1 = inv_del_tau_min
             end if

             b(1) = 1d0 + 2d0 * f1 * (1d0 + f1)
             c(1) = -2d0*f1**2d0
             a(1) = 0d0

             ! Calculate the local approximate lambda iterator
             lambda_loc(l,i,1) = lambda_loc(l,i,1) + &
                  w_gauss_mu(j)/(1d0 + 2d0 * f1 * (1d0 + f1))

             do k = 1+1, struc_len-1

                f1 = 2d0*mu(j)/(tau_approx_scat(l,i,k+1)-tau_approx_scat(l,i,k-1))
                f2 = mu(j)/(tau_approx_scat(l,i,k+1)-tau_approx_scat(l,i,k))
                f3 = mu(j)/(tau_approx_scat(l,i,k)-tau_approx_scat(l,i,k-1))

                ! own test against instability
                if (f1 > 0.5d0*inv_del_tau_min) then
                   f1 = 0.5d0*inv_del_tau_min
                end if
                if (f1 .NE. f1) then
                   f1 = 0.5d0*inv_del_tau_min
                end if
                if (f2 > inv_del_tau_min) then
                   f2 = inv_del_tau_min
                end if
                if (f2 .NE. f2) then
                   f2 = inv_del_tau_min
                end if
                if (f3 > inv_del_tau_min) then
                   f3 = inv_del_tau_min
                end if
                if (f3 .NE. f3) then
                   f3 = inv_del_tau_min
                end if

                b(k) = 1d0 + f1*(f2+f3)
                c(k) = -f1*f2
                a(k) = -f1*f3

                ! Calculate the local approximate lambda iterator
                lambda_loc(l,i,k) = lambda_loc(l,i,k) + &
                     w_gauss_mu(j)/(1d0+f1*(f2+f3))

             end do

             ! Own boundary treatment
             f1 = mu(j)/(tau_approx_scat(l,i,struc_len)-tau_approx_scat(l,i,struc_len-1))

             ! own test against instability
             if (f1 > inv_del_tau_min) then
                f1 = inv_del_tau_min
             end if
             if (f1 .NE. f1) then
                f1 = inv_del_tau_min
             end if

  !!$              b(struc_len) = 1d0 + 2d0*f1**2d0
  !!$              c(struc_len) = 0d0
  !!$              a(struc_len) = -2d0*f1**2d0
  !!$
  !!$              ! Calculate the local approximate lambda iterator
  !!$              lambda_loc(l,i,struc_len) = lambda_loc(l,i,struc_len) + &
  !!$                   w_gauss_mu(j)/(1d0 + 2d0*f1**2d0)

             ! TEST PAUL SCAT
             b(struc_len) = 1d0
             c(struc_len) = 0d0
             a(struc_len) = 0d0

             ! r(struc_len) = I_J(struc_len) = 0.5[I_plus + I_minus]
             ! where I_plus is the light that goes downwards and
             ! I_minus is the light that goes upwards.
             !!!!!!!!!!!!!!!!!! ALWAYS NEEDED !!!!!!!!!!!!!!!!!!
             I_plus = I_plus_surface(j, l, i)

                            !!!!!!!!!!!!!!! EMISSION ONLY TERM !!!!!!!!!!!!!!!!
             I_minus = surf_emi(i)*planck(struc_len) &
                           !!!!!!!!!!!!!!! SURFACE SCATTERING !!!!!!!!!!!!!!!!
                           ! ----> of the emitted/scattered atmospheric light
                           ! + surf_refl(i) * SUM(I_plus_surface(:, l, i) * w_gauss_mu) ! OLD PRE 091220
                           + surf_refl(i) * 2d0 * SUM(I_plus_surface(:, l, i) * mu * w_gauss_mu)
                           ! ----> of the direct stellar beam (depends on geometry)
             if  (trim(adjustl(geom)) .NE. 'non-isotropic') then
               I_minus = I_minus + surf_refl(i) &
                    ! * SUM(I_star_calc(l,:, struc_len, i) * w_gauss_mu) ! OLD PRE 091220
                    * 2d0 * SUM(I_star_calc(l,:, struc_len, i) * mu * w_gauss_mu)
             else
               !I_minus = I_minus + surf_refl(i) *J_star_ini(l,i,struc_len)  !to be checked! ! OLD PRE 091220
               I_minus = I_minus + surf_refl(i) *J_star_ini(l,i,struc_len) * 4d0 * mu_star
             end if

             !sum to get I_J
             r(struc_len)=0.5*(I_plus + I_minus)

             ! Calculate the local approximate lambda iterator
             lambda_loc(l,i,struc_len) = lambda_loc(l,i,struc_len) + &
                  w_gauss_mu(j)/(1d0 + 2d0*f1**2d0)

              call tridag_own(a,b,c,r,I_J(:,j),struc_len)

             I_H(1,j) = -I_J(1,j)

             do k = 1+1, struc_len-1
                f1 = mu(j)/(tau_approx_scat(l,i,k+1)-tau_approx_scat(l,i,k))
                f2 = mu(j)/(tau_approx_scat(l,i,k)-tau_approx_scat(l,i,k-1))
                if (f1 > inv_del_tau_min) then
                   f1 = inv_del_tau_min
                end if
                if (f2 > inv_del_tau_min) then
                   f2 = inv_del_tau_min
                end if
                deriv1 = f1*(I_J(k+1,j)-I_J(k,j))
                deriv2 = f2*(I_J(k,j)-I_J(k-1,j))
                I_H(k,j) = -(deriv1+deriv2)/2d0

                ! TEST PAUL SCAT
                if (k .EQ. struc_len - 1) then
                   I_plus_surface(j, l, i) = &
                        I_J(struc_len,j)  - deriv1
                end if
                ! END TEST PAUL SCAT
             end do

             I_H(struc_len,j) = 0d0

             ! TEST PAUL SCAT
             !I_plus_surface(j, l, i) = I_J(struc_len-1,j)+I_H(struc_len-1,j)
             ! END TEST PAUL SCAT

          end do

          J_bol_g = 0d0

          do j = 1, N_mu

             J_bol_g = J_bol_g + I_J(:,j) * w_gauss_mu(j)
             flux(i) = flux(i) - I_H(1,j)*mu(j) &
                  * 4d0*pi * w_gauss_ck(l) * w_gauss_mu(j)
          end do

          ! Save angle-dependent surface flux
          if (GCM_read) then
             do j = 1, N_mu
                I_GCM(j,i) = I_GCM(j,i) - 2d0*I_H(1,j)*w_gauss_ck(l)
             end do
          end if

          J_planet_scat(l,i,:) = J_bol_g

       end do

    end do

    do k = 1, struc_len
       do i = 1, freq_len_p_1-1
          do l = 1, N_g
             if (photon_destruct(l,i,k) < 1d-10) THEN
                photon_destruct(l,i,k) = 1d-10
             end if
          end do
       end do
    end do

    do i = 1, freq_len_p_1-1
       call planck_f_lr(struc_len,temp(1:struc_len),border_freqs(i),border_freqs(i+1),r)
       if (do_scat) then
           do l = 1, N_g
             source(l,i,:) = (photon_destruct(l,i,:)*r+(1d0-photon_destruct(l,i,:))* &
                   (J_star_ini(l,i,:)+J_planet_scat(l,i,:)-lambda_loc(l,i,:)*source(l,i,:))) / &
                   (1d0-(1d0-photon_destruct(l,i,:))*lambda_loc(l,i,:))
           end do
       end if
    end do

    conv_val = MAXVAL(ABS((I_GCM-I_GCM_old)/I_GCM))
    if ((conv_val < 1d-3) .AND. (i_iter_scat > 9)) then
        exit main_loop
    end if

    source_planet_scat_n3 = source_planet_scat_n2
    source_planet_scat_n2 = source_planet_scat_n1
    source_planet_scat_n1 = source_planet_scat_n
    source_planet_scat_n  = source

    if (mod(i_iter_scat,4) .EQ. 0) then
       !write(*,*) 'Ng acceleration!'
       call NG_source_approx(source_planet_scat_n,source_planet_scat_n1, &
            source_planet_scat_n2,source_planet_scat_n3,source, &
            N_g,freq_len_p_1,struc_len)
    end if
  end do main_loop !End scattering loop

end subroutine feautrier_rad_trans_phase_curve


!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

subroutine NG_source_approx(source_n,source_n1,source_n2,source_n3,source, &
     N_g,freq_len_p_1,struc_len)

  implicit none
  INTEGER :: struc_len, freq_len_p_1, N_g, i, i_ng, i_freq
  DOUBLE PRECISION :: tn(struc_len), tn1(struc_len), tn2(struc_len), &
       tn3(struc_len), temp_buff(struc_len), &
       source_n(N_g,freq_len_p_1-1,struc_len), source_n1(N_g,freq_len_p_1-1,struc_len), &
       source_n2(N_g,freq_len_p_1-1,struc_len), source_n3(N_g,freq_len_p_1-1,struc_len), &
       source(N_g,freq_len_p_1-1,struc_len), source_buff(N_g,freq_len_p_1-1,struc_len)
  DOUBLE PRECISION :: Q1(struc_len), Q2(struc_len), Q3(struc_len)
  DOUBLE PRECISION :: A1, A2, B1, B2, C1, C2
  DOUBLE PRECISION :: a, b

  do i_freq = 1, freq_len_p_1-1
     do i_ng = 1, N_g

        tn = source_n(i_ng,i_freq,1:struc_len)
        tn1 = source_n1(i_ng,i_freq,1:struc_len)
        tn2 = source_n2(i_ng,i_freq,1:struc_len)
        tn3 = source_n3(i_ng,i_freq,1:struc_len)

        Q1 = tn - 2d0*tn1 + tn2
        Q2 = tn - tn1 - tn2 + tn3
        Q3 = tn - tn1

        ! test
        Q1(1) = 0d0
        Q2(1) = 0d0
        Q3(1) = 0d0

        A1 = sum(Q1*Q1)
        A2 = sum(Q2*Q1)
        B1 = sum(Q1*Q2)
        B2 = sum(Q2*Q2)
        C1 = sum(Q1*Q3)
        C2 = sum(Q2*Q3)

        if ((abs(A1) >= 1d-250) .AND. &
             (abs(A2) >=1d-250) .AND. &
             (abs(B1) >=1d-250) .AND. &
             (abs(B2) >=1d-250) .AND. &
             (abs(C1) >=1d-250) .AND. &
             (abs(C2) >=1d-250)) THEN

           a = (C1*B2-C2*B1)/(A1*B2-A2*B1)
           b = (C2*A1-C1*A2)/(A1*B2-A2*B1)

           temp_buff = (1d0-a-b)*tn + a*tn1 + b*tn2

           do i = 1,struc_len
              if (temp_buff(i) <= 0d0) then
                 temp_buff(i) = 0d0
              end if
           end do

           do i = 1,struc_len
              if (temp_buff(i) .NE. temp_buff(i)) then
                 return
              end if
           end do

           source_buff(i_ng,i_freq,1:struc_len) = temp_buff

        else

           source_buff(i_ng,i_freq,1:struc_len) = source(i_ng,i_freq,1:struc_len)

        end if

     end do
  end do

  source = source_buff

end subroutine NG_source_approx

!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

! Tridag, own implementation, following the numerical recipes book.

subroutine tridag_own(a,b,c,res,solution,length)

  implicit none

  ! I/O
  integer, intent(in) :: length
  double precision, intent(in) :: a(length), &
       b(length), &
       c(length), &
       res(length)
  double precision, intent(out) :: solution(length)

  ! Internal variables
  integer :: ind
  double precision :: buffer_scalar, &
       buffer_vector(length)

  ! Test if b(1) == 0:
  if (b(1) .EQ. 0) then
     stop "Error in tridag routine, b(1) must not be zero!"
     end if

  ! Begin inversion
  buffer_scalar = b(1)
  solution(1) = res(1) / buffer_scalar

  do ind = 2, length
     buffer_vector(ind) = c(ind-1)/buffer_scalar
     buffer_scalar = b(ind) - a(ind) * buffer_vector(ind)
     if (buffer_scalar .EQ. 0) then
        write(*,*) "Tridag routine failed!"
        solution = 0d0
  return
     end if
     solution(ind) = (res(ind) - &
          a(ind)*solution(ind-1))/buffer_scalar
  end do

  do ind = length-1, 1, -1
     solution(ind) = solution(ind) &
          - buffer_vector(ind+1) * solution(ind + 1)
  end do

end subroutine tridag_own


!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

subroutine planck_f_lr(PT_length,T,nul,nur,B_nu)

  use constants_block
  implicit none
  INTEGER                         :: PT_length
  DOUBLE PRECISION                :: T(PT_length),B_nu(PT_length)
  DOUBLE PRECISION                ::  nu1, nu2, nu3, nu4, nu5, nu_large, nu_small, &
       nul, nur, diff_nu

  !~~~~~~~~~~~~~

  B_nu = 0d0
  ! Take mean using Boole's method
  nu_large = max(nul,nur)
  nu_small = min(nul,nur)
  nu1 = nu_small
  nu2 = nu_small+DBLE(1)*(nu_large-nu_small)/4d0
  nu3 = nu_small+DBLE(2)*(nu_large-nu_small)/4d0
  nu4 = nu_small+DBLE(3)*(nu_large-nu_small)/4d0
  nu5 = nu_large
  diff_nu = nu2-nu1
  B_nu = B_nu + 1d0/90d0*( &
       7d0* 2d0*hplanck*nu1**3d0/c_l**2d0/(exp(hplanck*nu1/kB/T)-1d0) + &
       32d0*2d0*hplanck*nu2**3d0/c_l**2d0/(exp(hplanck*nu2/kB/T)-1d0) + &
       12d0*2d0*hplanck*nu3**3d0/c_l**2d0/(exp(hplanck*nu3/kB/T)-1d0) + &
       32d0*2d0*hplanck*nu4**3d0/c_l**2d0/(exp(hplanck*nu4/kB/T)-1d0) + &
       7d0* 2d0*hplanck*nu5**3d0/c_l**2d0/(exp(hplanck*nu5/kB/T)-1d0))

end subroutine planck_f_lr

!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
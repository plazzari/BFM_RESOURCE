
! @author : epascolo, plazzari

subroutine init_bfm_derivative()

#include "BFM_module_list.h"

  implicit none

  call BFM0D_NO_BOXES(1,1,1,1,1)
  call BFM0D_INIT_IO_CHANNELS()
  call Initialize()

end subroutine init_bfm_derivative

subroutine dim_bfm_derivative(myidx)

#include "BFM_module_list.h"

implicit none

#include "BFM_var_list.h"
      INTEGER, intent(inout):: myidx(6)

      myidx(1)=jptra           ! Number of state variables
      myidx(2)=10              ! environmental reg. factors
      myidx(3)=jptra           ! Source Sinks / derivatives vector
      myidx(4)=4               ! Sinking velocities
      myidx(5)=jptra_dia       ! 3D diagnostics
      myidx(6)=jptra_dia_2d    ! 2D diagnostics

end subroutine dim_bfm_derivative

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


 subroutine calc_bfm_derivative(sur_in, bot_in,       &
                                st_in,  er_in,        &
                                so_out,               &
                                sv_out,di_out,di2_out)

!subroutine calc_bfm_derivative(sur_in, bot_in,             &
!                               st_in,  er_in,   st_b_in,    &
!                               so_out,so_b_out,             &
!                               sv_out,di_out,di2_out,       & 
!                               di_b_out,di2_b_out,          &
!                               di2_jsur_out, di2_jbot_out)

#include "BFM_module_list.h"

      implicit none

#include "BFM_var_list.h"

#if defined key_trc_benthic
#include "benthic_var_list.h"
#endif
      LOGICAL,intent (in)   :: sur_in,bot_in
      REAL(8), intent(in)   :: st_in(jptra),er_in(10)            ! Pelagic
      REAL(8), intent(inout):: so_out(jptra) !  Pelagic
      REAL(8),intent(inout) :: sv_out(4) ,di_out(jptra_dia) !  Pelagic
      REAL(8),intent(inout) :: di2_out(jptra_dia_2d) !  Pelagic

#if defined key_trc_benthic
      REAL(8), intent(in)  :: st_b_in(jptra_b)                  ! Benthic                 
      REAL(8)              :: so_b_out(jptra_b),di_b_out(jptra_dia_b)  ! Benthic                 
      REAL(8)              :: di2_b_out(jptra_dia_b_2d)
      REAL(8)              :: di2_jsur_out(jptra), di2_jbot_out(jptra)
#endif

      integer :: error=0

      call BFM0D_Input_EcologyDynamics(sur_in,bot_in,st_in,jptra,er_in)

#if defined key_trc_benthic
      if (bot) call BFM0D_Input_EcologyDynamics_benthic(st_b_in,jptra_b,er_in)
#endif

      call BFM0D_reset()

      call EcologyDynamics()

      if (sur_in) then
!     call BFM0D_Output_EcologyDynamics_surf(so_out, sv_out, di_out ,di2_out, di2_jsur_out)
      elseif(bot_in) then
!     call BFM0D_Output_EcologyDynamics_bot(so_out, sv_out, di_out ,di2_out, di2_jbot_out)
#if defined key_trc_benthic
      call BFM0D_output_EcologyDynamics_benthic(so_b_out,di_b_out,di2_b_out)
#endif
      else
      call BFM0D_Output_EcologyDynamics(so_out, sv_out, di_out)
      endif
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
end subroutine calc_bfm_derivative

subroutine finalize_bfm_derivative()

#include "BFM_module_list.h"

      call ClearMem()

end subroutine finalize_bfm_derivative

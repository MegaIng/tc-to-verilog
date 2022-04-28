`timescale 10ns / 1ns

module TC_Switch_testbench ();
    // clock and reset signals
//    reg clk;
//    reg rst;

    // dut (Design Under Test) io
    reg en0;
    reg en1;
    reg in0;
    reg in1;
    wire out;
    
    // dut instantiation
    TC_Switch dut0 (.en(en0), .in(in0), .out(out));
    TC_Switch dut1 (.en(en1), .in(in1), .out(out));

    // generate clock
//    initial begin
//        clk = 1'b0;
//        forever #1 clk = ~clk;
//    end

    // generate reset
//    initial begin
//        rst = 1'b1;
//        #10
//        rst = 1'b0;
//    end

    // run tests
    initial begin
        // monitor io
        $monitor("time=%3d, en0=%b, en1=%b, in0=%b, in1=%b, out=%b\n",
                    $time, en0, en1, in0, in1, out);
        
        // generate all input combinations with 200ns delays
		  en0 = 1'b0;
		  en1 = 1'b0;
        in0 = 1'b1;
        in1 = 1'b0;
        #20
        en0 = 1'b1;
        #20
        en0 = 1'b0;
        #20
        en1 = 1'b1;
        #20
        en1 = 1'b0;
		  #20
		  
		  in0 = 1'b0;
		  in1 = 1'b1;
        #20
        en0 = 1'b1;
        #20
        en0 = 1'b0;
        #20
        en1 = 1'b1;
        #20
        en1 = 1'b0;
		  #20
		  en0 = 1'b1;
		  en1 = 1'b1;
    end
endmodule


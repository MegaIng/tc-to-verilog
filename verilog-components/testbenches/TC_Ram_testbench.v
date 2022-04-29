`timescale 10ns / 1ns

module TC_Ram_testbench ();
    // clock and reset signals
    reg clk;
    reg rst;

    // dut (Design Under Test) io
    reg load;
    reg save;
    reg [7:0] address;
    reg [7:0] in;
    wire [7:0] out;
    
    // dut instantiation
    TC_Ram dut (.clk(clk), .rst(rst), .load(load), .save(save), .address(address), .in(in), .out(out));

    // generate clock
    initial begin
        clk = 1'b0;
        forever #1 clk = ~clk;
    end

    // generate reset
    initial begin
        rst = 1'b1;
        #10
        rst = 1'b0;
    end

    // run tests
    initial begin
        // monitor io
        $monitor("time=%3d, save=%b, load=%b, address=%8b, in=%8b, out=%8b\n",
                    $time, save, load, address, in, out);
        
        // generate all input combinations with 200ns delays
		load = 1'b0;
		save = 1'b0;
		address = 8'b0000_0000;
        in = 8'b0000_0000;
        #25
        address = 8'b0000_0000;
        in = 8'b0000_0001;
        save = 1'b1;
        #20
        save = 1'b0;
        #20
        load = 1'b1;
        #20
        load = 1'b0;
        #20
        address = 8'b0000_0001;
        in = 8'b0000_0010;
        save = 1'b1;
        #20
        save = 1'b0;
        #20
        load = 1'b1;
        #20
        load = 1'b0;
        #20
        address = 8'b0000_0000;
        load = 1'b1;
        #20
        load = 1'b0;
    end
endmodule

